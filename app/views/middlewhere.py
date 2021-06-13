import time
import logging

from aiohttp.web import middleware, HTTPFound
from aiohttp import BasicAuth, hdrs
from aiohttp_session import get_session


log = logging.getLogger(__name__)


def _do_basic_auth_check(request):
    auth_header = request.headers.get(hdrs.AUTHORIZATION)
    if not auth_header:
        return

    try:
        auth = BasicAuth.decode(auth_header=auth_header)
    except ValueError:
        auth = None

    if not auth:
        return

    if auth.login is None or auth.password is None:
        return

    return True


async def _do_cookies_auth_check(request):
    session = await get_session(request)
    if not session.get("logged_in", False):
        return

    session["last_at"] = time.time()
    return True


def middleware_factory():
    @middleware
    async def factory(request, handler):
        if request.app["is_authenticated"] and str(request.rel_url.path) not in [
            "/login",
            "/logout",
        ]:
            url = request.app.router["login_page"].url_for()
            if str(request.rel_url) != "/":
                url = url.with_query(redirect_to=str(request.rel_url))

            basic_auth_check_resp = _do_basic_auth_check(request)

            if basic_auth_check_resp is not None:
                return await handler(request)

            cookies_auth_check_resp = await _do_cookies_auth_check(request)

            if cookies_auth_check_resp is not None:
                return await handler(request)

            return HTTPFound(url)

        return await handler(request)

    return factory
