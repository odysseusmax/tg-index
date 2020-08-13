import random
import string

from aiohttp import web

from .config import chat_ids, alias_ids


def setup_routes(app, handler):
    h = handler
    routes =  [
        web.get('/', h.home, name='home')
    ]
    for chat_id in chat_ids:
        while True:
            alias_id = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(len(str(chat_id)))])
            if alias_id in alias_ids:
                continue
            alias_ids.append(alias_id)
            break
        p = f"/{alias_id}"
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
