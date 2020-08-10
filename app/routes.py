from aiohttp import web


def setup_routes(app, handler):
    h = handler
    app.add_routes(
        [
            web.get('/', h.index, name='index'),
            web.get(r"/{id:\d+}/view", h.info, name='info'),
            web.get(r"/{id:\d+}/download", h.download_get),
            web.head(r"/{id:\d+}/download", h.download_head),
            web.get(r"/{id:\d+}/thumbnail", h.thumbnail_get),
            web.head(r"/{id:\d+}/thumbnail", h.thumbnail_head),
        ]
    )
