import time

from aiohttp import web
import aiohttp_jinja2
from aiohttp_session import new_session


class LoginView:
    @aiohttp_jinja2.template("login.html")
    async def login_get(self, req):
        return dict(authenticated=False, **req.query)

    async def login_post(self, req):
        post_data = await req.post()
        redirect_to = post_data.get("redirect_to") or "/"
        location = req.app.router["login_page"].url_for()
        if redirect_to != "/":
            location = location.update_query({"redirect_to": redirect_to})

        if "username" not in post_data:
            loc = location.update_query({"error": "Username missing"})
            return web.HTTPFound(location=loc)

        if "password" not in post_data:
            loc = location.update_query({"error": "Password missing"})
            return web.HTTPFound(location=loc)

        authenticated = (post_data["username"] == req.app["username"]) and (
            post_data["password"] == req.app["password"]
        )
        if not authenticated:
            loc = location.update_query({"error": "Wrong Username or Passowrd"})
            return web.HTTPFound(location=loc)

        session = await new_session(req)
        print(session)
        session["logged_in"] = True
        session["logged_in_at"] = time.time()
        return web.HTTPFound(location=redirect_to)
