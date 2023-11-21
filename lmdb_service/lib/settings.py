import os
from uuid import uuid4


class BaseConfig:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", uuid4().hex)
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    LMBD_HOST = ""
    LMBD_HOST_POST_API = ""
