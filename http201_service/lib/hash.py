import base64
from hashlib import sha1
from random import Random
import marshal
import string


class RandomSequence(Random):
    """Generate random sequence and hash for the given url"""

    SEQUENCE_LENGTH = 7
    POPULATION = string.ascii_uppercase + string.ascii_lowercase + string.digits

    def __init__(self, long_url: str, hash: str | None = None) -> None:
        self.long_url = long_url
        self.hash: str = hash if hash else sha1(long_url.encode())
        self._sequence = None
        super()

    def update_sequence(self) -> None:
        self._sequence = "".join(
            self.choices(
                RandomSequence.POPULATION,
                k=RandomSequence.SEQUENCE_LENGTH,
            )
        )

    @property
    def sequence(self) -> str:
        if self._sequence is None:
            self.update_sequence()
        return self._sequence
