# pylint: disable=R0903:too-few-public-methods

import logging
import os
from enum import Enum
from logging.handlers import TimedRotatingFileHandler

from .formatter import JsonFormatter


class LevelName(Enum):
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class LoggerHandler:

    def __init__(self, level: int = LevelName.INFO):
        self.level = level.value

    def get_logger(self) -> logging.Logger:

        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        file_name = "licitador.log"
        full_file_path = os.path.join(log_dir, file_name)

        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger("licitador")

        if not logger.hasHandlers():
            logger.setLevel(self.level)

            formatter = JsonFormatter()

            file_handler = TimedRotatingFileHandler(
                full_file_path,
                when="midnight",
                interval=1,
                backupCount=7,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.level)

            logger.addHandler(file_handler)

        return logger
