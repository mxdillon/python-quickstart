import logging
import os
import sys

LOG_FILENAME = "logs.log"
LOG_LEVEL = logging.getLevelName(os.getenv("LOG_LEVEL", "DEBUG"))


# pylint: disable=too-few-public-methods
class LoggingMixin:
    """Mixin class for a consistent, custom logger.

    Usage:
        class Hello(LoggingMixin):
            def __init__(self) -> None:
                super().__init__()

            def hello(self, i=99):
                gg = 4 + 5 + i
                self.logger.warning(gg)
    """

    @property
    def logger(self) -> logging.Logger:
        """Helper function to generate custom logging.Logger class

        :return logging.Logger: custom logger object that can be called as
                                a property of the inheriting class
        """

        name = ".".join([self.__class__.__module__, self.__class__.__name__])
        logger = logging.getLogger(name)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s -  L%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler for stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(LOG_LEVEL)
        stream_handler.setFormatter(formatter)

        # Handler for log file
        file_handler = logging.FileHandler(filename=LOG_FILENAME, mode="a", encoding="utf-8")
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)

        # KEY LINE - if we don't check this we add new handlers to the logger ON EACH CALL!!
        # which leads to a bug where each successive nth log call repeats n times
        if not logger.hasHandlers():
            logger.addHandler(stream_handler)
            logger.addHandler(file_handler)

        return logger
