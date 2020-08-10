import math
import logging
import asyncio

from telethon import TelegramClient
from telethon.sessions import StringSession

class Client(TelegramClient):

    def __init__(self, session_string, *args, **kwargs):
        super().__init__(StringSession(session_string), *args, **kwargs)
        self.log = logging.getLogger(__name__)

    async def download(self, file, file_size, offset, limit):
        part_size = 1024 * 1024
        first_part_cut = offset % part_size
        first_part = math.floor(offset / part_size)
        last_part_cut = part_size - (limit % part_size)
        last_part = math.ceil(limit / part_size)
        part_count = math.ceil(file_size / part_size)
        part = first_part
        try:
            async for chunk in self.iter_download(file, offset=first_part * part_size, file_size=file_size, limit=part_size):
                if part == first_part:
                    yield chunk[first_part_cut:]
                elif part == last_part:
                    yield chunk[:last_part_cut]
                else:
                    yield chunk
                self.log.debug(f"Part {part}/{last_part} (total {part_count}) downloaded")
                part += 1
            self.log.debug("download finished")
        except (GeneratorExit, StopAsyncIteration, asyncio.CancelledError):
            self.log.debug("download interrupted")
            raise
        except Exception:
            self.log.debug("download errored", exc_info=True)