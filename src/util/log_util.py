import os
import logging

class LogUtil():

    def __init__(self):
        self.logger = logging.getLogger(os.getenv("LOG_NAME"))
        self.logger.setLevel(os.getenv("LOG_LEVEL"))
        handler = logging.FileHandler(filename=os.getenv("LOG_FILEPATH"), encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)
