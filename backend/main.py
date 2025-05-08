import uvicorn
from dotenv import load_dotenv

from config.settings import try_getenv

ENV_FILES = {
    "MAIN": "config/.env",
    "PROD": "config/.env.prod",
    "TEST": "config/.env.test",
    "DEV": "config/.env.dev",
}


def load_environment(mode: str):
    env_file = ENV_FILES.get(mode)
    load_dotenv(env_file)


def main():
    load_environment("MAIN")
    load_environment(try_getenv("APP_MODE"))

    uvicorn.run(
        "app:app",
        host=try_getenv("HOST"),
        port=int(try_getenv("PORT")),
        reload=try_getenv("RELOAD").lower() == "true",
        workers=5,
    )


if __name__ == "__main__":
    main()
