import random
import string

from .home_view import HomeView
from .wildcard_view import WildcardView
from .download import Download
from .index_view import IndexView
from .info_view import InfoView
from .logo_view import LogoView
from .thumbnail_view import ThumbnailView
from .login_view import LoginView
from .logout_view import LogoutView
from .middlewhere import middleware_factory


class Views(
    HomeView,
    Download,
    IndexView,
    InfoView,
    LogoView,
    ThumbnailView,
    WildcardView,
    LoginView,
    LogoutView,
):
    def __init__(self, client):
        self.client = client

        self.chat_ids = {}

    def generate_alias_id(self, chat):
        chat_id = chat.id
        title = chat.title
        while True:
            alias_id = "".join(
                [
                    random.choice(string.ascii_letters + string.digits)
                    for _ in range(len(str(chat_id)))
                ]
            )
            if alias_id in self.chat_ids:
                continue

            self.chat_ids[alias_id] = {
                "chat_id": chat_id,
                "alias_id": alias_id,
                "title": title,
            }

            return alias_id
