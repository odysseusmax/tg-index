import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

# os.system("alias python3=python")

def runSetup():
    def alert(missing):
        print(f"\nCopy your {missing} and save it as an environment variable.\n")

    req_env_vars = ["API_ID", "API_HASH", "INDEX_SETTINGS"]

    for env_var in req_env_vars:
        env_value = os.getenv(env_var)
        if env_value is None:
            alert(env_var)
            return

    if os.getenv("SESSION_STRRING") is None:
        os.system("python app/generate_session_string.py")
        print("\nCopy your SESSION_STRING from above and save it as an environment variable.")
        return

    os.system("python -m app")

if __name__ == "__main__":
    runSetup()
