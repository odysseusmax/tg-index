from aiohttp import web
import aiohttp_jinja2


class HomeView:

    @aiohttp_jinja2.template('home.html')
    async def home(self, req):
        if len(self.chat_ids) == 1:
            raise web.HTTPFound(f"{self.chat_ids[0]['alias_id']}")

        chats = []
        for chat in self.chat_ids:
            chats.append({
                'page_id': chat['alias_id'],
                'name': chat['title'],
                'url': f"/{chat['alias_id']}"
            })
        return {'chats': chats}
