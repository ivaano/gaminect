import logging
from datetime import datetime, timezone
from typing import Dict, Any
from pythonjsonlogger import jsonlogger

from app.core import config


class CustomJsonFormatter(jsonlogger.JsonFormatter):

    def add_fields(self,
                   log_record: Dict[str, Any],
                   record: logging.LogRecord,
                   message_dict: Dict[str, Any]) -> None:
        log_record['timestamp'] = datetime.fromtimestamp(record.created,
                                                         tz=timezone.utc)
        log_record['version'] = config.PROJECT_VERSION
        log_record['message'] = record.getMessage()
        log_record['logger_name'] = record.name
        log_record['thread_name'] = record.threadName
        log_record['level'] = record.levelname
        log_record['environment'] = config.ENVIRONMENT
        log_record['hostname'] = config.HOSTNAME
        log_record['uniq_service'] = config.SERVICE_NAME
        log_record.update(message_dict)
