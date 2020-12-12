import os

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.environ.get('API_ID') or input("Enter your API_ID: "))
api_hash = os.environ.get('API_HASH') or input("Enter your API_HASH: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
