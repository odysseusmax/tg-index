import asyncio
import pathlib
import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from .telegram import Client
from .routes import setup_routes
from .views import Views, middleware_factory
from .config import (
    host,
    port,
    session_string,
    api_id,
    api_hash,
    authenticated,
    username,
    password,
    SESSION_COOKIE_LIFETIME,
    SECRET_KEY,
)


log = logging.getLogger(__name__)


class Indexer:

    TEMPLATES_ROOT = pathlib.Path(__file__).parent / "templates"

    def __init__(self):
        middlewares = []
        if authenticated:
            middlewares.append(
                session_middleware(
                    EncryptedCookieStorage(
                        secret_key=SECRET_KEY.encode(),
                        max_age=60 * SESSION_COOKIE_LIFETIME,
                        cookie_name="TG_INDEX_SESSION",
                    )
                )
            )

        middlewares.append(middleware_factory())
        self.server = web.Application(middlewares=middlewares)
        self.loop = asyncio.get_event_loop()
        self.tg_client = Client(session_string, api_id, api_hash)

        self.server["is_authenticated"] = authenticated
        self.server["username"] = username
        self.server["password"] = password

    async def startup(self):
        await self.tg_client.start()
        log.debug("telegram client started!")

        await setup_routes(self.server, Views(self.tg_client))

        loader = jinja2.FileSystemLoader(str(self.TEMPLATES_ROOT))
        aiohttp_jinja2.setup(self.server, loader=loader)

        self.server.on_cleanup.append(self.cleanup)

    async def cleanup(self, *args):
        await self.tg_client.disconnect()
        log.debug("telegram client disconnected!")

    def run(self):
        self.loop.run_until_complete(self.startup())
        web.run_app(self.server, host=host, port=port)
