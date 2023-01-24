import os 
import runpy
import requests
import time
import psutil    
from dotenv import load_dotenv

load_dotenv()

APP_CMD = "python3 -m app"

def find_process_cmd(cmdline):
  for proc in psutil.process_iter():
    is_running = cmdline in proc.cmdline() 
    if(is_running):
      return True

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
      # proc = runpy.run_module('app', alter_sys=True)
      if(!find_process_cmd(APP_CMD)):
        # prevent running app if it is already running  
        print("Starting a new instance...")
        os.system(APP_CMD)
    else:
      print("Server is already running...")
  except Exception as e:
    os.system("python app/generate_session_string.py") 
  
def kill_server():
  print("Killing server just incase it is not responding...")
  kill_server_cmd = f"pkill -9 -f '{APP_CMD}'"
  os.system(kill_server_cmd)
  time.sleep(30)
    
run_safe()