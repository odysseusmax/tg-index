import random
import string
import logging

from aiohttp import web

from .config import index_settings, alias_ids, chat_ids


log = logging.getLogger(__name__)


def generate_alias_id(chat):
    chat_id = chat.id
    title = chat.title
    while True:
        alias_id = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(len(str(chat_id)))])
        if alias_id in alias_ids:
            continue
        alias_ids.append(alias_id)
        chat_ids.append({
            'chat_id': chat_id,
            'alias_id': alias_id,
            'title': title
        })
        return alias_id


async def setup_routes(app, handler):
    h = handler
    client = h.client
    p = r"/{chat:[^/]+}"
    routes =  [
        web.get('/', h.home),
        web.post('/otg', h.dynamic_view),
        web.get('/otg', h.otg_view),
        web.get(p, h.index),
        web.get(p + r"/logo", h.logo),
        web.get(p + r"/{id:\d+}/view", h.info),
        web.get(p + r"/{id:\d+}/download", h.download_get),
        web.head(p + r"/{id:\d+}/download", h.download_head),
        web.get(p + r"/{id:\d+}/thumbnail", h.thumbnail_get),
        web.view(r'/{wildcard:.*}', h.wildcard)
    ]
    index_all = index_settings['index_all']
    index_private = index_settings['index_private']
    index_group = index_settings['index_group']
    index_channel = index_settings['index_channel']
    exclude_chats = index_settings['exclude_chats']
    include_chats = index_settings['include_chats']
    if index_all:
        async for chat in client.iter_dialogs():
            alias_id = None
            if chat.id in exclude_chats:
                continue

            if chat.is_user:
                if index_private:
                    alias_id = generate_alias_id(chat)
            elif chat.is_channel:
                if index_channel:
                    alias_id = generate_alias_id(chat)
            else:
                if index_group:
                    alias_id = generate_alias_id(chat)

            if not alias_id:
                continue
            log.debug(f"Index added for {chat.id} :: {chat.title} at /{alias_id}")

    else:
        for chat_id in include_chats:
            chat = await client.get_entity(chat_id)
            alias_id = generate_alias_id(chat)
            log.debug(f"Index added for {chat.id} :: {chat.title} at /{alias_id}")

    app.add_routes(routes)
