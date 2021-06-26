import os
# from dotenv import load_dotenv

# load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

os.system("alias python3=python")


def runSetup():
    def alert(missing="API_ID , API_HASH"):
        print(
            f"\nCopy your {missing} and save it into Secrets(Environment variables) Sidebar!\n"
        )

    req_env_vars = ["API_ID", "API_HASH", "INDEX_SETTINGS"]
    misssing_envs = False
    for env_var in req_env_vars:
        env_value = os.getenv(env_var )
        if env_value is None:
             misssing_envs = True
             alert(env_var)
    
    if misssing_envs:
        return

    session_string = os.getenv("SESSION_STRING")
    if session_string is None:
        os.system("python app/generate_session_string.py")
        alert(missing="SESSION_STRING")
        return

    os.system("python -m app")


if __name__ == "__main__":
    runSetup()
