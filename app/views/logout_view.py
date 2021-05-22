from aiohttp import web


class LogoutView:
    async def logout_get(self, req):
        resp = web.Response(
            status=302, headers={"Location": str(req.app.router["home"].url_for())}
        )
        resp.del_cookie(name="_tgindex_session")
        resp.del_cookie(name="_tgindex_secret")
        return resp
