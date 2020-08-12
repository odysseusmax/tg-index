from aiohttp import web

from .config import chat_ids


def setup_routes(app, handler):
    h = handler
    routes =  [
        web.get('/', h.home, name='home')
    ]
    for chat_id in chat_ids:
        p = f"/{chat_id}"
        r = [
            web.get(p, h.index),
            web.get(p + r"/{id:\d+}/view", h.info),
            web.get(p + r"/{id:\d+}/download", h.download_get),
            web.head(p + r"/{id:\d+}/download", h.download_head),
            web.get(p + r"/{id:\d+}/thumbnail", h.thumbnail_get),
            web.head(p + r"/{id:\d+}/thumbnail", h.thumbnail_head),
        ]
        routes += r
    app.add_routes(routes)
