import sys
import logging
import logging.config

from app.core import config
from app.core.logging.filter import LogFilter
from app.core.logging.types import DictConfig

LOG_COLORS = (
    True
    if (value := config.LOG_COLORS)
    else False
    if value and value.lower() == "false"
    else sys.stdout.isatty()
)
LOG_FILTERS = LogFilter.set_filters()
LOG_FORMAT = config.LOG_FORMAT
LOG_LEVEL = str(config.LOG_LEVEL).upper()
LOGGING_CONFIG: DictConfig = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "filter_log_message": {"()": LogFilter, "filters": LOG_FILTERS},
    },
    "formatters": {
        "simple": {
            "class": "logging.Formatter",
            "format": "%(levelname)-10s %(message)s",
        },
        "verbose": {
            "class": "logging.Formatter",
            "format": (
                "%(asctime)-30s %(process)-10d %(name)-15s "
                "%(module)-15s %(levelname)-10s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        },
        "gunicorn": {
            "class": "logging.Formatter",
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
        },
        "uvicorn": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(levelprefix)s %(message)s",
            "use_colors": LOG_COLORS,
        },
        "json": {
            '()': 'app.core.logging.formatter.CustomJsonFormatter',
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "filters": ["filter_log_message"],
            "formatter": LOG_FORMAT,
            "level": LOG_LEVEL,
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"handlers": ["default"], "level": LOG_LEVEL},
    "loggers": {
        "fastapi": {"propagate": True},
        "gunicorn.access": {"handlers": ["default"], "propagate": True},
        "gunicorn.error": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"propagate": True},
        "uvicorn.asgi": {"propagate": True},
        "uvicorn.error": {"propagate": True},
        "sqlalchemy.engine.Engine": {"handlers": ["default"], "propagate": False},
    },
}


def configure_logging(
        logger: logging.Logger = logging.getLogger()
) -> DictConfig:
    """Configure Python logging given the name of a logging module or file."""
    try:
        logging_conf_path = __name__
        logging_conf_dict: DictConfig = LOGGING_CONFIG
        logging.config.dictConfig(logging_conf_dict)
        logger.debug(f"Logging dict config loaded from {logging_conf_path}.")
        return logging_conf_dict
    except Exception as e:
        logger.error(f"Error when setting logging module: {e.__class__.__name__} {e}.")
        raise
