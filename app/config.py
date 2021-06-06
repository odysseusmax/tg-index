from pathlib import Path
import platform
import traceback
import json
import sys
import os


try:
    port = int(os.environ.get("PORT", "8080"))
except ValueError:
    port = -1
if not 1 <= port <= 65535:
    print(
        "Please make sure the PORT environment variable is an integer between 1 and 65535"
    )
    sys.exit(1)

try:
    api_id = int(os.environ["API_ID"])
    api_hash = os.environ["API_HASH"]
except (KeyError, ValueError):
    traceback.print_exc()
    print("\n\nPlease set the API_ID and API_HASH environment variables correctly")
    print("You can get your own API keys at https://my.telegram.org/apps")
    sys.exit(1)

try:
    index_settings_str = os.environ["INDEX_SETTINGS"].strip()
    index_settings = json.loads(index_settings_str)
except:
    traceback.print_exc()
    print("\n\nPlease set the INDEX_SETTINGS environment variable correctly")
    sys.exit(1)

try:
    session_string = os.environ["SESSION_STRING"]
except (KeyError, ValueError):
    traceback.print_exc()
    print("\n\nPlease set the SESSION_STRING environment variable correctly")
    sys.exit(1)

host = os.environ.get("HOST", "0.0.0.0")
debug = bool(os.environ.get("DEBUG"))
block_downloads = bool(os.environ.get("BLOCK_DOWNLOADS"))
results_per_page = int(os.environ.get("RESULTS_PER_PAGE", "20"))
logo_folder = Path("./Temp/logo/" if platform.system() == "Windows" else "/tmp/logo")
if not logo_folder.exists():
    logo_folder.mkdir(parents=True)
username = os.environ.get("TGINDEX_USERNAME", "")
password = os.environ.get("PASSWORD", "")
SHORT_URL_LEN = int(os.environ.get("SHORT_URL_LEN", 3))
authenticated = username and password
SESSION_COOKIE_LIFETIME = int(os.environ.get("SESSION_COOKIE_LIFETIME") or "60")
try:
    SECRET_KEY = os.environ["SECRET_KEY"]
except (KeyError, ValueError):
    if authenticated:
        traceback.print_exc()
        print("\n\nPlease set the SECRET_KEY environment variable correctly")
        sys.exit(1)
    else:
        SECRET_KEY = ""
