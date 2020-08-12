import asyncio
import pathlib
import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web

from .telegram import Client
from .routes import setup_routes
from .views import Views
from .config import host, port, session_string, api_id, api_hash, debug


TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'
client = Client(session_string, api_id, api_hash)
logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
logging.getLogger("telethon").setLevel(logging.INFO if debug else logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.INFO if debug else logging.ERROR)
log = logging.getLogger("tg-index")


def setup_jinja(app):
    loader = jinja2.FileSystemLoader(str(TEMPLATES_ROOT))
    aiohttp_jinja2.setup(app, loader=loader)


async def start():
    await client.start()
    log.debug("telegram client started!")


async def stop(app):
    await client.disconnect()
    log.debug("telegram client disconnected!")


async def init():
    server = web.Application()
    await start()
    setup_routes(server, Views(client))
    setup_jinja(server)
    server.on_cleanup.append(stop)
    return server


def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init())
    web.run_app(app, host=host, port=port)


main()
