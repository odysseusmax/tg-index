import logging
from PIL import Image
import random
import io

from aiohttp import web
from telethon.tl import types, custom

from .base import BaseView


log = logging.getLogger(__name__)


class ThumbnailView(BaseView):
    async def thumbnail_get(self, req: web.Request) -> web.Response:
        file_id = int(req.match_info["id"])
        alias_id = req.match_info["chat"]
        chat = self.chat_ids[alias_id]
        chat_id = chat["chat_id"]
        try:
            message: custom.Message = await self.client.get_messages(
                entity=chat_id, ids=file_id
            )
        except Exception:
            log.debug(f"Error in getting message {file_id} in {chat_id}", exc_info=True)
            message = None

        if not message or not message.file:
            log.debug(f"no result for {file_id} in {chat_id}")
            return web.Response(
                status=410,
                text="410: Gone. Access to the target resource is no longer available!",
            )

        if message.document:
            media = message.document
            thumbnails = media.thumbs
            location = types.InputDocumentFileLocation
        else:
            media = message.photo
            thumbnails = media.sizes
            location = types.InputPhotoFileLocation

        if not thumbnails:
            color = tuple([random.randint(0, 255) for i in range(3)])
            im = Image.new("RGB", (100, 100), color)
            temp = io.BytesIO()
            im.save(temp, "PNG")
            body = temp.getvalue()
        else:
            thumb_pos = int(len(thumbnails) / 2)
            try:
                thumbnail: types.PhotoSize = self.client._get_thumb(
                    thumbnails, thumb_pos
                )
            except Exception as e:
                logging.debug(e)
                thumbnail = None

            if not thumbnail or isinstance(thumbnail, types.PhotoSizeEmpty):
                return web.Response(
                    status=410,
                    text="410: Gone. Access to the target resource is no longer available!",
                )

            if isinstance(thumbnail, (types.PhotoCachedSize, types.PhotoStrippedSize)):
                body = self.client._download_cached_photo_size(thumbnail, bytes)
            else:
                actual_file = location(
                    id=media.id,
                    access_hash=media.access_hash,
                    file_reference=media.file_reference,
                    thumb_size=thumbnail.type,
                )

                body = self.client.iter_download(actual_file)

        return web.Response(
            status=200,
            body=body,
            headers={
                "Content-Type": "image/jpeg",
                "Content-Disposition": 'inline; filename="thumbnail.jpg"',
            },
        )
