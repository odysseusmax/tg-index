import logging

import aiohttp_jinja2

from telethon.tl import types

from app.config import results_per_page
from app.util import get_file_name, get_human_size


log = logging.getLogger(__name__)


class IndexView:
    @aiohttp_jinja2.template("index.html")
    async def index(self, req):
        alias_id = req.match_info["chat"]
        chat = self.chat_ids[alias_id]
        log_msg = ""
        try:
            offset_val = int(req.query.get("page", "1"))
        except Exception:
            offset_val = 1

        log_msg += f"page: {offset_val} | "
        try:
            search_query = req.query.get("search", "")
        except Exception:
            search_query = ""

        log_msg += f"search query: {search_query} | "
        offset_val = 0 if offset_val <= 1 else offset_val - 1
        try:
            kwargs = {
                "entity": chat["chat_id"],
                "limit": results_per_page,
                "add_offset": results_per_page * offset_val,
            }
            if search_query:
                kwargs.update({"search": search_query})

            messages = (await self.client.get_messages(**kwargs)) or []

        except Exception:
            log.debug("failed to get messages", exc_info=True)
            messages = []

        log_msg += f"found {len(messages)} results | "
        log.debug(log_msg)
        results = []
        for m in messages:
            entry = None
            if m.file and not isinstance(m.media, types.MessageMediaWebPage):
                entry = dict(
                    file_id=m.id,
                    media=True,
                    thumbnail=f"/{alias_id}/{m.id}/thumbnail",
                    mime_type=m.file.mime_type,
                    insight=get_file_name(m),
                    human_size=get_human_size(m.file.size),
                    url=f"/{alias_id}/{m.id}/view",
                    download=f"{alias_id}/{m.id}/download",
                )
            elif m.message:
                entry = dict(
                    file_id=m.id,
                    media=False,
                    mime_type="text/plain",
                    insight=m.raw_text[:100],
                    url=f"/{alias_id}/{m.id}/view",
                )
            if entry:
                results.append(entry)

        prev_page = None
        next_page = None
        if offset_val:
            query = {"page": offset_val}
            if search_query:
                query.update({"search": search_query})
            prev_page = {"url": str(req.rel_url.with_query(query)), "no": offset_val}

        if len(messages) == results_per_page:
            query = {"page": offset_val + 2}
            if search_query:
                query.update({"search": search_query})
            next_page = {
                "url": str(req.rel_url.with_query(query)),
                "no": offset_val + 2,
            }

        return {
            "item_list": results,
            "prev_page": prev_page,
            "cur_page": offset_val + 1,
            "next_page": next_page,
            "search": search_query,
            "name": chat["title"],
            "logo": f"/{alias_id}/logo",
            "title": "Index of " + chat["title"],
            "authenticated": req.app["is_authenticated"],
        }
