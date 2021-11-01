from aiohttp import web
import aiohttp_jinja2

from .base import BaseView


class HomeView(BaseView):
    @aiohttp_jinja2.template("home.html")
    async def home(self, req: web.Request) -> web.Response:
        if len(self.chat_ids) == 1:
            (chat,) = self.chat_ids.values()
            return web.HTTPFound(f"{chat['alias_id']}")

        return {
            "chats": [
                {
                    "page_id": chat["alias_id"],
                    "name": chat["title"],
                    "url": f"/{chat['alias_id']}",
                }
                for _, chat in self.chat_ids.items()
            ],
            "authenticated": req.app["is_authenticated"],
        }
