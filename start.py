import importlib.util
import json
import logging
import subprocess
from pathlib import Path
import uvicorn

from app.core import config
from app.core.logging.config import configure_logging
from app.core.logging.types import DictConfig, UvicornOptions


def set_gunicorn_options(app_module: str) -> list[str]:
    """Set options for running the Gunicorn server."""
    gunicorn_conf_path = config.GUNICORN_CONF
    worker_class = config.WORKER_CLASS
    if "python:" not in gunicorn_conf_path and not Path(gunicorn_conf_path).is_file():
        raise FileNotFoundError(f"Unable to find {gunicorn_conf_path}")
    return ["gunicorn", "-k", worker_class, "-c", gunicorn_conf_path, app_module]


def _update_uvicorn_options(uvicorn_options: UvicornOptions) -> UvicornOptions:
    if uvicorn.__version__ >= "0.15.0":
        uvicorn_options["reload_delay"] = config.RELOAD_DELAY
        uvicorn_options["reload_includes"] = _split_uvicorn_option(config.RELOAD_EXCLUDES)
        uvicorn_options["reload_excludes"] = _split_uvicorn_option(config.RELOAD_INCLUDES)
    if value := config.UVICORN_CONFIG_OPTIONS:
        uvicorn_options_json = json.loads(value)
        uvicorn_options.update(uvicorn_options_json)
    return uvicorn_options


def _split_uvicorn_option(option: str) -> list[str] | None:
    return (
        [option_item.strip() for option_item in str(option_value).split(sep=",")]
        if (option_value := option)
        else None
    )


def set_uvicorn_options(
        app_module: str,
        log_config: DictConfig | None = None,
) -> UvicornOptions:
    """Set options for running the Uvicorn server."""
    host = config.HOST
    port = config.PORT
    log_level = config.LOG_LEVEL
    reload_dirs = _split_uvicorn_option(config.RELOAD_DIRS)
    use_reload = config.WITH_RELOAD
    uvicorn_options: UvicornOptions = dict(
        app=app_module,
        host=host,
        port=port,
        log_config=log_config,
        log_level=log_level,
        reload=use_reload,
        reload_dirs=reload_dirs,
    )
    return _update_uvicorn_options(uvicorn_options)


def set_app_module(_logger: logging.Logger = logging.getLogger()) -> str:
    """Set the name of the Python module with the app instance to run."""
    try:
        app_module = config.APP_MODULE
        if not app_module:
            raise ValueError("Please set the APP_MODULE environment variable")
        if not importlib.util.find_spec((module := app_module.split(sep=":")[0])):
            raise ImportError(f"Unable to find or import {module}")
        _logger.debug(f"App module set to {app_module}.")
        return app_module
    except Exception as e:
        _logger.error(f"Error when setting app module: {e.__class__.__name__} {e}.")
        raise


def start_server(
        process_manager: str,
        app_module: str,
        _logger: logging.Logger = logging.getLogger(),
        _logging_conf_dict: DictConfig | None = None,
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    try:
        if process_manager == "gunicorn":
            _logger.debug("Running Uvicorn with Gunicorn.")
            gunicorn_options: list[str] = set_gunicorn_options(app_module)
            subprocess.run(gunicorn_options)
        elif process_manager == "uvicorn":
            _logger.debug("Running Uvicorn without Gunicorn.")
            uvicorn_options: UvicornOptions = set_uvicorn_options(
                app_module, log_config=_logging_conf_dict
            )
            uvicorn.run(**uvicorn_options)  # type: ignore[arg-type]
        else:
            raise NameError("Process manager needs to be either uvicorn or gunicorn")
    except Exception as e:
        logger.error(f"Error when starting server: {e.__class__.__name__} {e}.")
        raise


if __name__ == "__main__":  # pragma: no cover
    logger = logging.getLogger()
    logging_conf_dict = configure_logging(logger=logger)
    start_server(
        str(config.PROCESS_MANAGER),
        app_module=set_app_module(_logger=logger),
        _logger=logger,
        _logging_conf_dict=logging_conf_dict,
    )
