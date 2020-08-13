import logging

from aiohttp import web
import aiohttp_jinja2
from jinja2 import Markup
from telethon.tl import types
from telethon.tl.custom import Message

from .util import get_file_name, get_human_size
from .config import chat_ids, alias_ids


log = logging.getLogger(__name__)


class Views:
    
    def __init__(self, client):
        self.client = client
    
    
    @aiohttp_jinja2.template('home.html')
    async def home(self, req):
        if len(chat_ids) == 1:
            raise web.HTTPFound(f"{alias_ids[0]}")
        chats = []
        for chat_id, alias_id in zip(chat_ids, alias_ids):
            chat = await self.client.get_entity(chat_id)
            chats.append({
                'id': alias_id,
                'name': chat.title
            })
        return {'chats':chats}
    

    @aiohttp_jinja2.template('index.html')
    async def index(self, req):
        alias_id = req.rel_url.path.split('/')[1]
        chat_id = chat_ids[alias_ids.index(alias_id)]
        chat = await self.client.get_entity(chat_id)
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
            if m.file and not isinstance(m.media, types.MessageMediaWebPage):
                entry = dict(
                    file_id=m.id,
                    media=True,
                    mime_type=m.file.mime_type,
                    insight = get_file_name(m)[:55],
                    date = m.date.isoformat(),
                    size=get_human_size(m.file.size),
                    url=req.rel_url.with_path(f"/{alias_id}/{m.id}/view")
                )
            elif m.message:
                entry = dict(
                    file_id=m.id,
                    media=False,
                    mime_type='text/plain',
                    insight = m.raw_text[:55],
                    date = m.date.isoformat(),
                    size=get_human_size(len(m.raw_text)),
                    url=req.rel_url.with_path(f"/{alias_id}/{m.id}/view")
                )
            results.append(entry)
        prev_page = False
        next_page = False
        if offset_val:
            query = {'page':offset_val}
            if search_query:
                query.update({'search':search_query})
            prev_page =  {
                'url': req.rel_url.with_query(query),
                'no': offset_val
            }
        
        if len(messages)==20:
            query = {'page':offset_val+2}
            if search_query:
                query.update({'search':search_query})
            next_page =  {
                'url': req.rel_url.with_query(query),
                'no': offset_val+2
            }

        return {
            'item_list':results, 
            'prev_page': prev_page,
            'cur_page' : offset_val+1,
            'next_page': next_page,
            'search': search_query,
            'name' : chat.title
        }


    @aiohttp_jinja2.template('info.html')
    async def info(self, req):
        file_id = int(req.match_info["id"])
        alias_id = req.rel_url.path.split('/')[1]
        chat_id = chat_ids[alias_ids.index(alias_id)]
        message = await self.client.get_messages(entity=chat_id, ids=file_id)
        if not message or not isinstance(message, Message):
            log.debug(f"no valid entry for {file_id} in {chat_id}")
            return {
                'found':False,
                'reason' : "Entry you are looking for cannot be retrived!",
            }
        return_val = {}
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
                caption = Markup.escape(message.raw_text).__str__().replace('\n', '<br>')
                
            else:
                caption = False
            return_val = {
                'found': True,
                'name': file_name,
                'id': file_id,
                'size': file_size,
                'media': media,
                'caption': caption,
                'title': f"Download | {file_name} | {file_size}" 
            }
        elif message.message:
            text = Markup.escape(message.raw_text).__str__().replace('\n', '<br>')
            return_val = {
                'found': True,
                'media': False,
                'text': text,
            }
        else:
            return_val = {
                'found':False,
                'reason' : "Some kind of entry that I cannot display",
            }
        
        log.debug(f"data for {file_id} in {chat_id} returned as {return_val}")
        return return_val
        
    
    async def download_get(self, req):
        return await self.handle_request(req)
    
    
    async def download_head(self, req):
        return await self.handle_request(req, head=True)
    
    
    async def thumbnail_get(self, req):
        return await self.handle_request(req, thumb=True)
    

    async def thumbnail_head(self, req):
        return await self.handle_request(req, head=True, thumb=True)


    async def handle_request(self, req, head=False, thumb=False):
        file_id = int(req.match_info["id"])
        alias_id = req.rel_url.path.split('/')[1]
        chat_id = chat_ids[alias_ids.index(alias_id)]
        message = await self.client.get_messages(entity=chat_id, ids=file_id)
        if not message or not message.file:
            log.info(f"no result for {file_id} in {chat_id}")
            return web.Response(status=410, text="410: Gone. Access to the target resource is no longer available!")
        
        if thumb and message.document:
            thumbnail = message.document.thumbs
            if not thumbnail:
                log.info(f"no thumbnail for {file_id} in {chat_id}")
                return web.Response(status=404, text="404: Not Found")
            thumbnail = thumbnail[-1]
            mime_type = 'image/jpeg'
            size = thumbnail.size
            file_name = f"{file_id}_thumbnail.jpg"
            media = types.InputDocumentFileLocation(
                id=message.document.id,
                access_hash=message.document.access_hash,
                file_reference=message.document.file_reference,
                thumb_size=thumbnail.type
            )
        else:
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
            log.info("Range Not Satisfiable", exc_info=True)
            return web.Response(
                status=416,
                text="416: Range Not Satisfiable",
                headers = {
                    "Content-Range": f"bytes */{size}"
                }
            )
        
        body = None
        if not head:
            body = self.client.download(media, size, offset, limit)
            log.info(f"Serving file {message.id} in {chat_id} ; Range: {offset} - {limit}")
        
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
