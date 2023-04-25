import os
import socket


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


def getenv(var_name, default_value=None):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value
    return result


PROJECT_NAME = "Gameinect"
PROJECT_DESCRIPTION = "Web UI for playnite data."
PROJECT_VERSION = '0.1'
API_VERSION_STR = "/api/v1"


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
PROCESS_MANAGER = os.getenv("PROCESS_MANAGER", "uvicorn")  # gunicorn or uvicorn
APP_MODULE = os.getenv("APP_MODULE", "app.main:app")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
HOSTNAME = value if (value := os.getenv("DOCKER_HOST_NAME")) else socket.gethostname()
SERVICE_NAME = os.getenv("SERVICE_NAME", "gameinect")
BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)

docs = None
redoc = None
if ENVIRONMENT == "development":
    docs = "/docs"
    redoc = "/redoc"

DOCS_URL = os.getenv("DOCS_URL", docs)  # disabled by default for dev set this to "/docs"
REDOC_URL = os.getenv("REDOC_URL", redoc)  # "/redoc"



# uvicorn settings
UVICORN_CONFIG_OPTIONS = os.getenv("UVICORN_CONFIG_OPTIONS")  # additional json settings for uvicorn
WITH_RELOAD = getenv_boolean("WITH_RELOAD", False)
RELOAD_DIRS = os.getenv("RELOAD_DIRS")
RELOAD_DELAY = float(value) if (value := os.getenv("RELOAD_DELAY")) else 0.25
RELOAD_EXCLUDES = os.getenv("RELOAD_EXCLUDES")
RELOAD_INCLUDES = os.getenv("RELOAD_INCLUDES")

# gunicorn settings
GUNICORN_CONF = os.getenv("GUNICORN_CONF", "python:app.core.gunicorn_conf")
WORKER_CLASS = os.getenv("WORKER_CLASS", "uvicorn.workers.UvicornWorker")

# log settings
LOG_COLORS = getenv_boolean("LOG_COLORS", False)
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # simple, verbose, uvicorn or json
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")  # critical, error, warning, info, debug, trace
LOG_FILTERS = os.getenv("LOG_FILTERS", "/health")
