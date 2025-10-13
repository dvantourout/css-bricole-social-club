from starlette.config import Config
from starlette.datastructures import Secret

config = Config("../.env")

DATABASE_HOST = config("DATABASE_HOST")
DATABASE_PORT = config("DATABASE_PORT", default=5432)
DATABASE_USER = config("DATABASE_USER", cast=Secret)
DATABASE_PASSWORD = config("DATABASE_PASSWORD", cast=Secret)
DATABASE_NAME = config("DATABASE_NAME")

SQLALCHEMY_URI = f"postgresql+psycopg://{str(DATABASE_USER)}:{str(DATABASE_PASSWORD)}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
