import random
import string

from telethon.utils import get_display_name

from .home_view import HomeView
from .wildcard_view import WildcardView
from .download import Download
from .index_view import IndexView
from .info_view import InfoView
from .logo_view import LogoView
from .thumbnail_view import ThumbnailView


class Views(HomeView, Download,
            IndexView, InfoView,
            LogoView, ThumbnailView,
            WildcardView):

    def __init__(self, client):
        self.client = client

        self.alias_ids = []
        self.chat_ids = []

    def generate_alias_id(self, chat):
        chat_id = chat.id
        title = chat.title
        while True:
            alias_id = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(len(str(chat_id)))])
            if alias_id in self.alias_ids:
                continue
            self.alias_ids.append(alias_id)
            self.chat_ids.append({
                'chat_id': chat_id,
                'alias_id': alias_id,
                'title': title
            })
            return alias_id
