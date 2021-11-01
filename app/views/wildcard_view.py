from aiohttp import web

from .base import BaseView


class WildcardView(BaseView):
    async def wildcard(self, req: web.Request) -> web.Response:
        return web.HTTPFound("/")
