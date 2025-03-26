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

        fmtr = logging.Formatter("[{asctime}] [{levelname:<7}] {message}", "%Y-%m-%d %H:%M:%S", style="{")

        hdlr = RotatingFileHandler(
            filename="logs/bot.log",
            maxBytes=5 * 1024 * 1024,  # 5 MiB
            backupCount=5,
            encoding="utf-8",
        )
        hdlr.setFormatter(fmtr)

        self.addHandler(hdlr)
