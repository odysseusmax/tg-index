import logging
from PIL import Image, ImageDraw, ImageFont
import random

from aiohttp import web
from telethon.tl import types

from app.config import logo_folder


log = logging.getLogger(__name__)


class LogoView:
    async def logo(self, req):
        alias_id = req.match_info["chat"]
        chat = self.chat_ids[alias_id]
        chat_id = chat["chat_id"]
        chat_name = " ".join(map(lambda x: x[0].upper(), chat["title"].split(" ")))
        logo_path = logo_folder.joinpath(f"{alias_id}.jpg")
        if not logo_path.exists():
            try:
                (photo,) = await self.client.get_profile_photos(chat_id, limit=1)
            except Exception:
                log.debug(
                    f"Error in getting profile picture in {chat_id}", exc_info=True
                )
                photo = None

            if not photo:
                W, H = (360, 360)
                color = tuple((random.randint(0, 255) for _ in range(3)))
                im = Image.new("RGB", (W, H), color)
                draw = ImageDraw.Draw(im)
                font = ImageFont.truetype("arial.ttf", 50)
                w, h = draw.textsize(chat_name, font=font)
                draw.text(
                    ((W - w) / 2, (H - h) / 2), chat_name, fill="white", font=font
                )
                im.save(logo_path)
            else:
                pos = -1 if req.query.get("big", None) else int(len(photo.sizes) / 2)
                size = self.client._get_thumb(photo.sizes, pos)
                if isinstance(size, (types.PhotoCachedSize, types.PhotoStrippedSize)):
                    await self.client._download_cached_photo_size(size, logo_path)
                else:
                    media = types.InputPhotoFileLocation(
                        id=photo.id,
                        access_hash=photo.access_hash,
                        file_reference=photo.file_reference,
                        thumb_size=size.type,
                    )
                    await self.client.download_file(media, logo_path)

        with open(logo_path, "rb") as fp:
            body = fp.read()

        return web.Response(
            status=200,
            body=body,
            headers={
                "Content-Type": "image/jpeg",
                "Content-Disposition": 'inline; filename="logo.jpg"',
            },
        )
