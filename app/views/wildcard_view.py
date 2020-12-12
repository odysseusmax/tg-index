from aiohttp import web


class WildcardView:

    async def wildcard(self, req):
        raise web.HTTPFound('/')
