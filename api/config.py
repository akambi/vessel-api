
import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database/database.db")
    DATABASE_URL_COPY = os.getenv("DATABASE_URL_COPY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False