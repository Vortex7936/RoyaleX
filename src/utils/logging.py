import os
import logging
from logging.handlers import RotatingFileHandler


class Logger(logging.Logger):
    def __init__(self, name: str):
        level = logging._nameToLevel.get(
            os.getenv("LOG_LEVEL", "").upper(),
            logging.INFO,
        )
        super().__init__(name=name, level=level)

        # Remove existing handlers to avoid duplication
        if self.hasHandlers():
            for hdlr in self.handlers[:]:
                self.removeHandler(hdlr)
                hdlr.close()

        formatter = logging.Formatter(
            fmt="[{asctime}] [{levelname:<7}] {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )

        # Ensure log directory exists
        filename = os.getenv("LOG_FILE_PATH", "logs/bot.log")
        logs_dir = os.path.dirname(filename)

        if logs_dir:
            os.makedirs(logs_dir, exist_ok=True)

        handler = RotatingFileHandler(
            filename=filename,
            maxBytes=5 * 1024 * 1024,  # 5 MiB
            backupCount=5,
            encoding="utf-8",
        )
        handler.setFormatter(formatter)

        self.addHandler(handler)
