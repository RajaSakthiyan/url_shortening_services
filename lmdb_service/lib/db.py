import marshal
from flask import Flask
import lmdb

DEFAULT_DB_PATH = "alias_db"


class DBOperation:
    def __init__(self, app: Flask) -> None:
        db_path: str = app.config.get("DB_PATH", DEFAULT_DB_PATH)
        self.lmdb_env: lmdb.Environment = lmdb.open(db_path)

    @staticmethod
    def decode_data(data: bytes) -> tuple[str, str]:
        long_url, code = marshal.loads(data)
        return long_url, code

    @staticmethod
    def encode_data(long_url: str, code: str) -> bytes:
        data = (long_url, code)
        return marshal.dumps(data)

    def do_put(self, hash: bytes, code: bytes, data: bytes) -> bytes | None:
        value = bytes | None
        with self.lmdb_env.begin(write=True) as txn:
            value: bytes | None = txn.get(hash, default=None)
            if not value:
                txn.put(hash, data)
                txn.put(code, hash)
        return value

    def do_get(self, code: bytes) -> tuple[bytes, bytes] | None:
        data = bytes | None
        hash = bytes | None
        with self.lmdb_env.begin() as txn:
            hash: bytes | None = txn.get(code, default=None)
            if hash:
                data: bytes | None = txn.get(hash, default=None)
        return data, hash

    def put_data(self, alias_data: dict) -> dict | None:
        try:
            hash: bytes = alias_data["hash"].encode()
            bcode: bytes = alias_data["code"].encode()
            data: bytes = self.encode_data(alias_data["long_url"], alias_data["code"])
            value: bytes | None = self.do_put(hash, bcode, data)
            long_url, code = (
                self.decode_data(value)
                if value
                else [alias_data["long_url"], alias_data["code"]]
            )
            return {"code": code, "hash": alias_data["hash"], "long_url": long_url}
        except Exception:
            return None

    def get_data(self, code: str) -> dict | None:
        try:
            code: bytes = code.encode()
            data, hash = self.do_get(code)
            if hash and data:
                long_url, code = self.decode_data(data)
                return {"code": code, "hash": hash.decode(), "long_url": long_url}
            return {"hash": None, "code": None, "long_url": None}
        except Exception:
            return None
