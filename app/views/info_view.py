import logging

import aiohttp_jinja2
from telethon.tl import types
from telethon.tl.custom import Message
from jinja2 import Markup

from app.util import get_file_name, get_human_size


log = logging.getLogger(__name__)


class InfoView:

    @aiohttp_jinja2.template('info.html')
    async def info(self, req):
        file_id = int(req.match_info["id"])
        alias_id = req.match_info['chat']
        chat = [i for i in self.chat_ids if i['alias_id'] == alias_id][0]
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
                'reason' : "Resource you are looking for cannot be retrived!",
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
            human_file_size = get_human_size(message.file.size)
            media = {
                'type':message.file.mime_type
            }
            if 'video/' in message.file.mime_type:
                media['video'] : True
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
                'file_id': file_id,
                'human_size': human_file_size,
                'media': media,
                'caption_html': caption_html,
                'title': f"Download | {file_name} | {human_file_size}",
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
                'text_html': text_html,
                'reply_btns': reply_btns,
                'page_id': alias_id
            }
        else:
            return_val = {
                'found':False,
                'reason' : "Some kind of resource that I cannot display",
            }
        log.debug(f"data for {file_id} in {chat_id} returned as {return_val}")
        return return_val
