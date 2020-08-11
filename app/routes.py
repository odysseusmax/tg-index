from aiohttp import web


def setup_routes(app, handler):
    h = handler
    app.add_routes(
        [
            web.get("/", h.new_index, name='new_index'),
            web.get(r"/{chat_id}/", h.index, name='index'),
            web.get(r"/{chat_id}/{id:\d+}/view", h.info, name='info'),
            web.get(r"/{chat_id}/{id:\d+}/download", h.download_get),
            web.head(r"/{chat_id}/{id:\d+}/download", h.download_head),
            web.get(r"/{chat_id}/{id:\d+}/thumbnail", h.thumbnail_get),
            web.head(r"/{chat_id}/{id:\d+}/thumbnail", h.thumbnail_head),
        ]
    )
