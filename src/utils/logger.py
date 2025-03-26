import os
import logging
from logging.handlers import RotatingFileHandler


class Logger(logging.Logger):
    def __init__(self):
        name_ = os.getenv("LOG_NAME", "root")
        level = logging._nameToLevel.get(
            os.getenv("LOG_LEVEL", "").upper(),
            logging.INFO,
        )
        super().__init__(name=name_, level=level)

        # Remove existing handlers to avoid duplication
        if self.hasHandlers():
            for hdlr in self.handlers[:]:
                self.removeHandler(hdlr)
                hdlr.close()

        formatter = logging.Formatter(
            fmt="[{asctime}] [{levelname:<7}] {name}: {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )

        handler = RotatingFileHandler(
            filename=os.getenv("LOG_FILEPATH", "bot.log"),
            maxBytes=5 * 1024 * 1024,  # 5 MiB
            backupCount=5,
            encoding="utf-8",
        )
        handler.setFormatter(formatter)

        self.addHandler(handler)
