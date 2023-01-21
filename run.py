import os 
import runpy
import requests
import time
from dotenv import load_dotenv
load_dotenv()

def is_alive():
  repl_slug = os.environ.get("REPL_SLUG")
  repl_owner = os.environ.get("REPL_OWNER")
  repl_url = f"https://{repl_slug}.{repl_owner}.repl.co"
  repl_url_local = "http://0.0.0.0:8080"
  try:
    resp = requests.get(repl_url_local, timeout=60)
  except Exception as e:
    print("Server response wait timed out!")
    return False
  return resp.ok

def run_safe():
  "prevent session string from expiring due to two instances running"
  try:
    if not is_alive():
      kill_server()
      print("Starting a new instance...")
      # runpy.run_module('app', run_name="tgindex")
      os.system("python3 -m app")
    else:
      print("Server is already running...")
  except Exception as e:
    print(f"Your session String has been revoked due to {e}. \n\n Please generate New one.")
    os.system("python app/generate_session_string.py") 
  
def kill_server():
  print("Killing server just incase it is not responding...")
  kill_server_cmd = "pkill -9 -f 'python3 -m app'"
  os.system(kill_server_cmd)
  time.sleep(5)
    
run_safe()