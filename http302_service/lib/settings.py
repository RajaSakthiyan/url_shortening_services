import os
from uuid import uuid4


class BaseConfig:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", uuid4().hex)
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    LMBD_HOST = "http://127.0.0.1:8083"
    LMBD_HOST_GET_API = "/get"
