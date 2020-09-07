import logging
from PIL import Image, ImageDraw, ImageFont
import random
import io

from aiohttp import web
import aiohttp_jinja2
from jinja2 import Markup
from telethon.tl import types
from telethon.tl.custom import Message

from .util import get_file_name, get_human_size
from .config import index_settings, chat_ids


log = logging.getLogger(__name__)


class Views:
    
    def __init__(self, client):
        self.client = client
    
    
    async def _home(self, req):
        chats = []
        for chat in chat_ids:
            chats.append({
                'id': chat['alias_id'],
                'name': chat['title'],
                'url': req.rel_url.path + f"/{chat['alias_id']}"
            })
        return {'chats':chats}
    

    @aiohttp_jinja2.template('home.html')
    async def home(self, req):
        if len(chat_ids) == 1:
            raise web.HTTPFound(f"{chat_ids[0]['alias_id']}")
        return await self._home(req)
    
    
    async def api_home(self, req):
        data = await self._home(req)
        return web.json_response(data)


    @aiohttp_jinja2.template('index.html')
    async def index(self, req):
        return await self._index(req)
    
    
    async def api_index(self, req):
        data = await self._index(req, True)
        return web.json_response(data)
    
    
    async def _index(self, req, api=False):
        alias_pos = 2 if api else 1
        alias_id = req.rel_url.path.split('/')[alias_pos]
        chat = [i for i in chat_ids if i['alias_id'] == alias_id][0]
        chat_id = chat['chat_id']
        chat_name = chat['title']
        log_msg = ''
        try:
            offset_val = int(req.query.get('page', '1'))
        except:
            offset_val = 1
        log_msg += f"page: {offset_val} | "
        try:
            search_query = req.query.get('search', '')
        except:
            search_query = ''
        log_msg += f"search query: {search_query} | "
        offset_val = 0 if offset_val <=1 else offset_val-1
        try:
            kwargs = {
                'entity': chat_id,
                'limit': 20,
                'add_offset': 20*offset_val
            }
            if search_query:
                kwargs.update({'search': search_query})
            messages = (await self.client.get_messages(**kwargs)) or []
            
        except:
            log.debug("failed to get messages", exc_info=True)
            messages = []
        log_msg += f"found {len(messages)} results | "
        log.debug(log_msg)
        results = []
        for m in messages:
            entry = None
            if m.file and not isinstance(m.media, types.MessageMediaWebPage):
                entry = dict(
                    file_id=m.id,
                    media=True,
                    thumbnail=f"/{alias_id}/{m.id}/thumbnail",
                    mime_type=m.file.mime_type,
                    insight = get_file_name(m)[:100],
                    date = str(m.date),
                    size=get_human_size(m.file.size),
                    url=req.rel_url.path + f"/{m.id}/view"
                )
            elif m.message:
                entry = dict(
                    file_id=m.id,
                    media=False,
                    mime_type='text/plain',
                    insight = m.raw_text[:100],
                    date = str(m.date),
                    size=get_human_size(len(m.raw_text)),
                    url=req.rel_url.path + f"/{m.id}/view"
                )
            if entry:
                results.append(entry)
        prev_page = False
        next_page = False
        if offset_val:
            query = {'page':offset_val}
            if search_query:
                query.update({'search':search_query})
            prev_page =  {
                'url': str(req.rel_url.with_query(query)),
                'no': offset_val
            }
        
        if len(messages)==20:
            query = {'page':offset_val+2}
            if search_query:
                query.update({'search':search_query})
            next_page =  {
                'url': str(req.rel_url.with_query(query)),
                'no': offset_val+2
            }

        return {
            'item_list':results, 
            'prev_page': prev_page,
            'cur_page' : offset_val+1,
            'next_page': next_page,
            'search': search_query,
            'name' : chat['title'],
            'logo': f"/{alias_id}/logo",
            'title' : "Index of " + chat_name
        }


    @aiohttp_jinja2.template('info.html')
    async def info(self, req):
        return await self._info(req)
    
    
    async def api_info(self, req):
        data = await self._info(req, True)
        if not data['found']:
            return web.Response(status=404, text="404: Not Found")
        
        return web.json_response(data)
        
        
    async def _info(self, req, api=False):
        file_id = int(req.match_info["id"])
        alias_pos = 2 if api else 1
        alias_id = req.rel_url.path.split('/')[alias_pos]
        chat = [i for i in chat_ids if i['alias_id'] == alias_id][0]
        chat_id = chat['chat_id']
        try:
            message = await self.client.get_messages(entity=chat_id, ids=file_id)
        except:
            log.debug(f"Error in getting message {file_id} in {chat_id}", exc_info=True)
            message = None
        if not message or not isinstance(message, Message):
            log.debug(f"no valid entry for {file_id} in {chat_id}")
            return {
                'found':False,
                'reason' : "Entry you are looking for cannot be retrived!",
            }
        return_val = {}
        reply_btns = []
        if message.reply_markup:
            if isinstance(message.reply_markup, types.ReplyInlineMarkup):
                for button_row in message.reply_markup.rows:
                    btns = []
                    for button in button_row.buttons:
                        if isinstance(button, types.KeyboardButtonUrl):
                            btns.append({'url': button.url, 'text': button.text})
                    reply_btns.append(btns)
        if message.file and not isinstance(message.media, types.MessageMediaWebPage):
            file_name = get_file_name(message)
            file_size = get_human_size(message.file.size)
            media = {
                'type':message.file.mime_type
            }
            if 'video/' in message.file.mime_type:
                media.update({
                    'video' : True
                })
            elif 'audio/' in message.file.mime_type:
                media['audio'] = True
            elif 'image/' in message.file.mime_type:
                media['image'] = True
                
            if message.text:
                caption = message.raw_text
            else:
                caption = ''
            caption_html = Markup.escape(caption).__str__().replace('\n', '<br>')
            return_val = {
                'found': True,
                'name': file_name,
                'id': file_id,
                'size': file_size,
                'media': media,
                'caption_html': caption_html,
                'caption': caption,
                'title': f"Download | {file_name} | {file_size}",
                'reply_btns': reply_btns,
                'thumbnail': f"/{alias_id}/{file_id}/thumbnail",
                'download_url': f"/{alias_id}/{file_id}/download",
                'page_id': alias_id
            }
        elif message.message:
            text = message.raw_text
            text_html = Markup.escape(text).__str__().replace('\n', '<br>')
            return_val = {
                'found': True,
                'media': False,
                'text': text,
                'text_html': text_html,
                'reply_btns': reply_btns,
                'page_id': alias_id
            }
        else:
            return_val = {
                'found':False,
                'reason' : "Some kind of entry that I cannot display",
            }
        log.debug(f"data for {file_id} in {chat_id} returned as {return_val}")
        return return_val
    

    async def logo(self, req):
        alias_id = req.rel_url.path.split('/')[1]
        chat = [i for i in chat_ids if i['alias_id'] == alias_id][0]
        chat_id = chat['chat_id']
        chat_name = "Image not available"
        try:
            photo = await self.client.get_profile_photos(chat_id)
        except:
            log.debug(f"Error in getting profile picture in {chat_id}", exc_info=True)
            photo = None
        if not photo:
            W, H = (160, 160)
            c = lambda : random.randint(0, 255)
            color = tuple([c() for i in range(3)])
            im = Image.new("RGB", (W,H), color)
            draw = ImageDraw.Draw(im)
            w, h = draw.textsize(chat_name)
            draw.text(((W-w)/2,(H-h)/2), chat_name, fill="white")
            temp = io.BytesIO()
            im.save(temp, "PNG")
            body = temp.getvalue()
        else:
            photo = photo[0]
            pos = -1 if req.query.get('big', None) else int(len(photo.sizes)/2)
            size = self.client._get_thumb(photo.sizes, pos)
            if isinstance(size, (types.PhotoCachedSize, types.PhotoStrippedSize)):
                body = self.client._download_cached_photo_size(size, bytes)
            else:
                media = types.InputPhotoFileLocation(
                    id=photo.id,
                    access_hash=photo.access_hash,
                    file_reference=photo.file_reference,
                    thumb_size=size.type
                )
                body = self.client.iter_download(media)
        
        r = web.Response(
            status=200,
            body=body,
        )
        #r.enable_chunked_encoding()
        return r
    
    
    async def download_get(self, req):
        return await self.handle_request(req)
    
    
    async def download_head(self, req):
        return await self.handle_request(req, head=True)
    
    
    async def thumbnail_get(self, req):
        file_id = int(req.match_info["id"])
        alias_id = req.rel_url.path.split('/')[1]
        chat = [i for i in chat_ids if i['alias_id'] == alias_id][0]
        chat_id = chat['chat_id']
        try:
            message = await self.client.get_messages(entity=chat_id, ids=file_id)
        except:
            log.debug(f"Error in getting message {file_id} in {chat_id}", exc_info=True)
            message = None
        
        if not message or not message.file:
            log.debug(f"no result for {file_id} in {chat_id}")
            return web.Response(status=410, text="410: Gone. Access to the target resource is no longer available!")
        
        if message.document:
            media = message.document
            thumbnails = media.thumbs
            location = types.InputDocumentFileLocation
        else:
            media = message.photo
            thumbnails = media.sizes
            location = types.InputPhotoFileLocation
        
        if not thumbnails:
            c = lambda : random.randint(0, 255)
            color = tuple([c() for i in range(3)])
            im = Image.new("RGB", (100, 100), color)
            temp = io.BytesIO()
            im.save(temp, "PNG")
            body = temp.getvalue()
        else:
            thumb_pos = int(len(thumbnails)/2)
            thumbnail = self.client._get_thumb(thumbnails, thumb_pos)
            if not thumbnail or isinstance(thumbnail, types.PhotoSizeEmpty):
                return web.Response(status=410, text="410: Gone. Access to the target resource is no longer available!")
            
            if isinstance(thumbnail, (types.PhotoCachedSize, types.PhotoStrippedSize)):
                body = self.client._download_cached_photo_size(thumbnail, bytes)
            else:
                actual_file = location(
                    id=media.id,
                    access_hash=media.access_hash,
                    file_reference=media.file_reference,
                    thumb_size=thumbnail.type
                )
            
                body = self.client.iter_download(actual_file)
        
        r = web.Response(
            status=200,
            body=body,
        )
        r.enable_chunked_encoding()
        return r
    

    async def handle_request(self, req, head=False):
        file_id = int(req.match_info["id"])
        alias_id = req.rel_url.path.split('/')[1]
        chat = [i for i in chat_ids if i['alias_id'] == alias_id][0]
        chat_id = chat['chat_id']
        
        try:
            message = await self.client.get_messages(entity=chat_id, ids=file_id)
        except:
            log.debug(f"Error in getting message {file_id} in {chat_id}", exc_info=True)
            message = None
        
        if not message or not message.file:
            log.debug(f"no result for {file_id} in {chat_id}")
            return web.Response(status=410, text="410: Gone. Access to the target resource is no longer available!")
        
        media = message.media
        size = message.file.size
        file_name = get_file_name(message)
        mime_type = message.file.mime_type
        
        try:
            offset = req.http_range.start or 0
            limit = req.http_range.stop or size
            if (limit > size) or (offset < 0) or (limit < offset):
                raise ValueError("range not in acceptable format")
        except ValueError:
            return web.Response(
                status=416,
                text="416: Range Not Satisfiable",
                headers = {
                    "Content-Range": f"bytes */{size}"
                }
            )
        
        if not head:
            body = self.client.download(media, size, offset, limit)
            log.info(f"Serving file in {message.id} (chat {chat_id}) ; Range: {offset} - {limit}")
        else:
            body = None
        
        headers = {
            "Content-Type": mime_type,
            "Content-Range": f"bytes {offset}-{limit}/{size}",
            "Content-Length": str(limit - offset),
            "Accept-Ranges": "bytes",
            "Content-Disposition": f'attachment; filename="{file_name}"'
        }

        return web.Response(
            status=206 if offset else 200,
            body=body,
            headers=headers
        )
