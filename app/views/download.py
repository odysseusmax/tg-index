import logging

from aiohttp import web

from app.util import get_file_name
from app.config import block_downloads


log = logging.getLogger(__name__)


class Download:
    async def download_get(self, req):
        return await self.handle_request(req)

    async def download_head(self, req):
        return await self.handle_request(req, head=True)

    async def handle_request(self, req, head=False):
        if block_downloads:
            return web.Response(status=403, text="403: Forbiden" if not head else None)

        file_id = int(req.match_info["id"])
        alias_id = req.match_info["chat"]
        chat = self.chat_ids[alias_id]
        chat_id = chat["chat_id"]

        try:
            message = await self.client.get_messages(entity=chat_id, ids=file_id)
        except Exception:
            log.debug(f"Error in getting message {file_id} in {chat_id}", exc_info=True)
            message = None

        if not message or not message.file:
            log.debug(f"no result for {file_id} in {chat_id}")
            return web.Response(
                status=410,
                text="410: Gone. Access to the target resource is no longer available!"
                if not head
                else None,
            )

        media = message.media
        size = message.file.size
        file_name = get_file_name(message, quote_name=False)
        mime_type = message.file.mime_type

        try:
            offset = req.http_range.start or 0
            limit = req.http_range.stop or size
            if (limit > size) or (offset < 0) or (limit < offset):
                raise ValueError("range not in acceptable format")
        except ValueError:
            return web.Response(
                status=416,
                text="416: Range Not Satisfiable" if not head else None,
                headers={"Content-Range": f"bytes */{size}"},
            )

        if not head:
            body = self.client.download(media, size, offset, limit)
            log.info(
                f"Serving file in {message.id} (chat {chat_id}) ; Range: {offset} - {limit}"
            )
        else:
            body = None

        headers = {
            "Content-Type": mime_type,
            "Content-Range": f"bytes {offset}-{limit}/{size}",
            "Content-Length": str(limit - offset),
            "Accept-Ranges": "bytes",
            "Content-Disposition": f'attachment; filename="{file_name}"',
        }

        return web.Response(status=206 if offset else 200, body=body, headers=headers)
