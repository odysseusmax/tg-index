import logging
from typing import List

from aiohttp import web
from aiohttp.web_routedef import RouteDef
from telethon.tl.types import Channel, Chat, User

from .config import index_settings
from .views import Views

log = logging.getLogger(__name__)


def get_common_routes(handler: Views, alias_id: str) -> List[RouteDef]:
    p = "/{chat:" + alias_id + "}"
    return [
        web.get(p, handler.index, name=f"index_{alias_id}"),
        web.get(p + r"/logo", handler.logo, name=f"logo_{alias_id}"),
        web.get(p + r"/{id:\d+}/view", handler.info, name=f"info_{alias_id}"),
        web.get(
            p + r"/{id:\d+}/thumbnail",
            handler.thumbnail_get,
            name=f"thumbnail_get_{alias_id}",
        ),
        web.get(
            p + r"/{id:\d+}/{filename}",
            handler.download_get,
            name=f"download_get_{alias_id}",
        ),
        web.head(
            p + r"/{id:\d+}/{filename}",
            handler.download_head,
            name=f"download_head_{alias_id}",
        ),
    ]


async def setup_routes(app: web.Application, handler: Views):
    client = handler.client
    index_all = index_settings["index_all"]
    index_private = index_settings["index_private"]
    index_group = index_settings["index_group"]
    index_channel = index_settings["index_channel"]
    exclude_chats = index_settings["exclude_chats"]
    include_chats = index_settings["include_chats"]
    routes = [
        web.get("/", handler.home, name="home"),
        web.get("/login", handler.login_get, name="login_page"),
        web.post("/login", handler.login_post, name="login_handle"),
        web.get("/logout", handler.logout_get, name="logout"),
        web.get("/favicon.ico", handler.faviconicon, name="favicon"),
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

            alias_id = handler.generate_alias_id(chat)
            routes.extend(get_common_routes(handler, alias_id))
            log.debug(f"Index added for {chat.id} at /{alias_id}")

    else:
        for chat_id in include_chats:
            chat = await client.get_entity(chat_id)
            alias_id = handler.generate_alias_id(chat)
            routes.extend(
                get_common_routes(handler, alias_id)
            )  # returns list() of common routes
            log.debug(f"Index added for {chat.id} at /{alias_id}")
    routes.append(web.view(r"/{wildcard:.*}", handler.wildcard, name="wildcard"))
    app.add_routes(routes)
