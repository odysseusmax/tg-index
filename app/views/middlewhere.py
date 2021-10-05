import time
import logging

from aiohttp.web import middleware, HTTPFound, Response
from aiohttp import BasicAuth, hdrs
from aiohttp_session import get_session


log = logging.getLogger(__name__)


def _do_basic_auth_check(request):
    if "download_" not in request.match_info.route.name:
        return

    auth = None
    auth_header = request.headers.get(hdrs.AUTHORIZATION)
    if auth_header is not None:
        try:
            auth = BasicAuth.decode(auth_header=auth_header)
        except ValueError:
            pass

    if auth is None:
        try:
            auth = BasicAuth.from_url(request.url)
        except ValueError:
            pass

    if not auth:
        return Response(
            body=b"",
            status=401,
            reason="UNAUTHORIZED",
            headers={hdrs.WWW_AUTHENTICATE: 'Basic realm=""'},
        )

    if auth.login is None or auth.password is None:
        return

    if (
        auth.login != request.app["username"]
        or auth.password != request.app["password"]
    ):
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
        if not request.app["is_authenticated"] or str(request.rel_url.path) in [
            "/login",
            "/logout",
            "/favicon.ico",
        ]:
            return await handler(request)
        url = request.app.router["login_page"].url_for()
        if str(request.rel_url) != "/":
            url = url.with_query(redirect_to=str(request.rel_url))

        basic_auth_check_resp = _do_basic_auth_check(request)

        if basic_auth_check_resp is True:
            return await handler(request)

        cookies_auth_check_resp = await _do_cookies_auth_check(request)

        if cookies_auth_check_resp is not None:
            return await handler(request)

        if isinstance(basic_auth_check_resp, Response):
            return basic_auth_check_resp

        return HTTPFound(url)

    return factory
