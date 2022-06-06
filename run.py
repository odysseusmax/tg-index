import os 
import runpy
import requests
from dotenv import load_dotenv
load_dotenv()

def is_alive():
  repl_slug = os.environ.get("REPL_SLUG")
  repl_owner = os.environ.get("REPL_OWNER")
  try:
    resp = requests.get(f"https://{repl_slug}.{repl_owner}.repl.co", timeout=15)
  except Exception as e:
    print("Server response wait timed out!")
    return False
  return resp.ok

def run_safe():
  "prevent session string from expiring due to two instances running"
  if not is_alive():
    print("Starting a new instance...")
    runpy.run_module('app')
  else:
    print("Server is already running...")

def kill_server():
  kill_server_cmd = "pkill -9 -f 'python3 run.py'"
  os.system(kill_server_cmd)
    
run_safe()