from typing import Dict, Union

from telethon.tl.types import Chat, User, Channel

from ..telegram import Client


TELEGRAM_CHAT = Union[Chat, User, Channel]


class BaseView:
    client: Client
    url_len: int
    chat_ids: Dict[str, Dict[str, str]]
