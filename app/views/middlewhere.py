import time
import hmac
import hashlib
import logging

from aiohttp.web import middleware, HTTPFound


log = logging.getLogger(__name__)


def middleware_factory():
    @middleware
    async def factory(request, handler):
        if request.app["is_authenticated"] and str(request.rel_url.path) not in [
            "/login",
            "/logout",
        ]:
            cookies = request.cookies
            url = request.app.router["login_page"].url_for()
            if str(request.rel_url) != "/":
                url = url.with_query(redirect_to=str(request.rel_url))

            if any(x not in cookies for x in ("_tgindex_session", "_tgindex_secret")):
                raise HTTPFound(url)

            tgindex_session = cookies["_tgindex_session"]
            tgindex_secret = cookies["_tgindex_secret"]
            calculated_digest = hmac.new(
                request.app["SECRET_KEY"].encode(),
                str(tgindex_session).encode(),
                hashlib.sha256,
            ).hexdigest()
            if tgindex_secret != calculated_digest:
                raise HTTPFound(url)

            try:
                created_at = (
                    float(tgindex_session) + request.app["SESSION_COOKIE_LIFETIME"]
                )
                if (
                    time.time()
                    > created_at + 60 * request.app["SESSION_COOKIE_LIFETIME"]
                ):
                    raise HTTPFound(url)
            except Exception as e:
                log.error(e, exc_info=True)
                raise HTTPFound(url)

        return await handler(request)

    return factory
