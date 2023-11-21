from typing import TypeAlias
from flask import Flask
import requests

URL_ALIAS: TypeAlias = dict[str, dict[str, str]]

DEFAULT_HEADER = {"content-type": "application/json"}


class DBError(Exception):
    pass


class RemoteLMDB:
    def __init__(self, app: Flask) -> None:
        host = app.config.get("LMBD_HOST", "http://none")
        get_api = app.config.get("LMBD_HOST_GET_API", "")
        self.db_get_api = host + get_api

    def get_long_url(self, alias_code: str) -> URL_ALIAS:
        try:
            response: requests.Response = requests.get(
                f"{self.db_get_api}/{alias_code}", headers=DEFAULT_HEADER
            )
            if response.status_code == 200:
                alias_data: dict = response.json()
                return {
                    "code": alias_data["code"],
                    "id": alias_data["hash"],
                    "long_url": alias_data["long_url"],
                }
            else:
                raise DBError("Unable to get long url")
        except requests.exceptions.RequestException as e:
            raise DBError("DB service is not running")
