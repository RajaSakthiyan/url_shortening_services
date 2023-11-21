import base64
from hashlib import sha1
import hashlib
from random import Random
import marshal
import string


class HashSequence:
    """Generate sequence encoding hash for the given url"""

    SEQUENCE_LENGTH = 7
    ALPHA_NUM = string.ascii_uppercase + string.ascii_lowercase + string.digits

    def __init__(self, long_url: str, hash: str | None = None) -> None:
        self.long_url = long_url
        self._hash: str = hash if hash else sha1(long_url.encode())
        self._sequence = None
        super()

    def encode_hash(self) -> None:
        ecoded_hash = base64.b85encode(self._hash.digest())
        self._sequence = "".join(
            filter(lambda x: x in HashSequence.ALPHA_NUM, ecoded_hash.decode())
        )[: HashSequence.SEQUENCE_LENGTH]

    @property
    def sequence(self) -> str:
        if self._sequence is None:
            self.encode_hash()
        return self._sequence

    @property
    def hash(self) -> str:
        return self._hash.hexdigest()
