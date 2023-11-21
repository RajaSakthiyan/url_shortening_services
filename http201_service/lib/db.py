from typing import TypeAlias
from flask import Flask
import requests

from lib.hash import RandomSequence

URL_ALIAS: TypeAlias = dict[str, dict[str, str]]

DEFAULT_HEADER = {"content-type": "application/json"}


class DBError(Exception):
    pass


class RemoteLMDB:
    def __init__(self, app: Flask) -> None:
        host = app.config.get("LMBD_HOST", "http://none")
        post_api = app.config.get("LMBD_HOST_POST_API", "")
        self.db_post_api = host + post_api

    def create_alias(self, long_url: str) -> URL_ALIAS:
        try:
            random_sequence = RandomSequence(long_url)
            post_data: dict = {
                "hash": random_sequence.hash,
                "code": random_sequence.sequence,
                "long_url": random_sequence.long_url,
            }
            response: requests.Response = requests.post(
                self.db_post_api, data=post_data, headers=DEFAULT_HEADER
            )
            if response.status_code == 201:
                alias_data: dict = response.json()
                return {
                    "code": alias_data["code"],
                    "long_url": alias_data["long_url"],
                    "id": alias_data["hash"],
                }
            else:
                raise DBError("Unable to create short url")
        except requests.exceptions.RequestException as e:
            raise DBError("DB service is not running")
