import sys
from .get_cfg import get_config


try:
    port = int(get_config("PORT", "8080"))
except ValueError:
    port = -1
if not 1 <= port <= 65535:
    print(
        "Please make sure the PORT environment variable is "
        "an integer between 1 and 65535"
    )
    sys.exit(1)

api_id = int(get_config(
    "API_ID",
    should_prompt=True
))
api_hash = get_config(
    "API_HASH",
    should_prompt=True,
    error_message=(
        "Please set the API_ID and API_HASH environment variables correctly\n"
        "You can get your own API keys at https://my.telegram.org/apps"
    )
)

# array to store the channel ID who are authorized to use the bot
chat_id = list(set(
    int(x) for x in get_config(
        "CHAT_ID",
        should_prompt=True,
        error_message=(
            "Please set the CHAT_ID environment variable correctly"
        )
    ).split()
))

session_string = get_config(
    "SESSION_STRING",
    should_prompt=True,
    error_message=(
        "Please set the SESSION_STRING environment variable correctly"
    )
)

host = get_config("HOST", "0.0.0.0")
debug = bool(get_config("DEBUG"))
