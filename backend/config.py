import logging

from starlette.config import Config
from starlette.datastructures import Secret

config = Config("../.env")

DATABASE_HOST = config("DATABASE_HOST")
DATABASE_PORT = config("DATABASE_PORT", default=5432)
DATABASE_USER = config("DATABASE_USER", cast=Secret)
DATABASE_PASSWORD = config("DATABASE_PASSWORD", cast=Secret)
DATABASE_NAME = config("DATABASE_NAME")

SQLALCHEMY_URI = f"postgresql+psycopg://{str(DATABASE_USER)}:{str(DATABASE_PASSWORD)}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Define format for logs
fmt = "%(asctime)s | %(levelname)8s | %(message)s"

# Create stdout handler for logging to the console (logs all five levels)
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(fmt))
