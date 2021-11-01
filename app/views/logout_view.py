from aiohttp_session import get_session
from aiohttp import web

from .base import BaseView


class LogoutView(BaseView):
    async def logout_get(self, req: web.Request) -> web.Response:
        session = await get_session(req)
        session["logged_in"] = False

        return web.HTTPFound(req.app.router["home"].url_for())
