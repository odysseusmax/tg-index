import logging

from aiohttp import web
from telethon.tl.types import Channel, Chat, User

from .config import index_settings

log = logging.getLogger(__name__)

async def setup_routes(app, handler):
    h = handler
    client = h.client
    index_all = index_settings["index_all"]
    index_private = index_settings["index_private"]
    index_group = index_settings["index_group"]
    index_channel = index_settings["index_channel"]
    exclude_chats = index_settings["exclude_chats"]
    include_chats = index_settings["include_chats"]
    routes = [
        web.get("/", h.home, name="home"),
        web.get("/login", h.login_get, name="login_page"),
        web.post("/login", h.login_post, name="login_handle"),
        web.get("/logout", h.logout_get, name="logout"),
    ]
    def get_common_routes(p):
        return [
                    web.get(p, h.index),
                    web.get(p + r"/logo", h.logo),
                    web.get(p + r"/{id:\d+}/view", h.info),
                    web.get(p + r"/{id:\d+}/download", h.download_get),
                    web.head(p + r"/{id:\d+}/download", h.download_head),
                    web.get(p + r"/{id:\d+}/thumbnail", h.thumbnail_get),
                    web.get(p + r"/{id:\d+}/v.mp4", h.download_get),
                    web.head(p + r"/{id:\d+}/v.mp4", h.download_head),
                ]
    if index_all:
        # print(await client.get_dialogs())
        # dialogs = await client.get_dialogs()
        # for chat in dialogs:
        async for chat in client.iter_dialogs():
            alias_id = None
            if chat.id in exclude_chats:
                continue

            entity = chat.entity

            if isinstance(entity, User) and not index_private:
                log.debug(f"{chat.title}, private: {index_private}")
                continue
            elif isinstance(entity, Channel) and not index_channel:
                log.debug(f"{chat.title}, channel: {index_channel}")
                continue
            elif isinstance(entity, Chat) and not index_group:
                log.debug(f"{chat.title}, group: {index_group}")
                continue

            alias_id = h.generate_alias_id(chat)
            p = "/{chat:" + alias_id + "}"
            routes.extend(
               get_common_routes(p)
            )
            log.debug(f"Index added for {chat.id} at /{alias_id}")

    else:
        for chat_id in include_chats:
            chat = await client.get_entity(chat_id)
            alias_id = h.generate_alias_id(chat)
            p = "/{chat:" + alias_id + "}"
            routes.extend(
                get_common_routes(p) # returns list() of common routes 
            )
            log.debug(f"Index added for {chat.id} at /{alias_id}")
    routes.append(web.view(r"/{wildcard:.*}", h.wildcard))
    app.add_routes(routes)
