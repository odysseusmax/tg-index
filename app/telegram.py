import math
import logging
import asyncio

from telethon import TelegramClient, utils
from telethon.sessions import StringSession


class Client(TelegramClient):
    def __init__(self, session_string, *args, **kwargs):
        super().__init__(StringSession(session_string), *args, **kwargs)
        self.log = logging.getLogger(__name__)

    async def download(self, file, file_size, offset, limit):
        part_size = utils.get_appropriated_part_size(file_size) * 1024
        first_part_cut = offset % part_size
        first_part = math.floor(offset / part_size)
        last_part_cut = part_size - (limit % part_size)
        last_part = math.ceil(limit / part_size)
        part_count = math.ceil(file_size / part_size)
        part = first_part
        self.log.debug(
            f"""Request Details
              part_size(bytes) = {part_size},
              first_part = {first_part}, cut = {first_part_cut}(length={part_size-first_part_cut}),
              last_part = {last_part}, cut = {last_part_cut}(length={last_part_cut}),
              parts_count = {part_count}
              """
        )
        try:
            async for chunk in self.iter_download(
                file, offset=first_part * part_size, request_size=part_size
            ):
                self.log.debug(f"Part {part}/{last_part} (total {part_count}) served!")
                if part == first_part:
                    yield chunk[first_part_cut:]
                elif part == last_part:
                    yield chunk[:last_part_cut]
                    break
                else:
                    yield chunk

                part += 1

            self.log.debug(f"serving finished")
        except (GeneratorExit, StopAsyncIteration, asyncio.CancelledError):
            self.log.debug("file serve interrupted")
            raise
        except Exception:
            self.log.debug("file serve errored", exc_info=True)
