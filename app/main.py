import asyncio
import pathlib
import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web

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
        self.server = web.Application(
            middlewares=[
                middleware_factory(),
            ]
        )
        self.loop = asyncio.get_event_loop()
        self.tg_client = Client(session_string, api_id, api_hash)

        self.server["is_authenticated"] = authenticated
        self.server["username"] = username
        self.server["password"] = password
        self.server["SESSION_COOKIE_LIFETIME"] = SESSION_COOKIE_LIFETIME
        self.server["SECRET_KEY"] = SECRET_KEY

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
