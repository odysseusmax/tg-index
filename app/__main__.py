import logging

from .main import Indexer
from .config import debug


logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
logging.getLogger("telethon").setLevel(logging.INFO if debug else logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.INFO if debug else logging.ERROR)


Indexer().run()
