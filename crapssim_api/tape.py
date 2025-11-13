import json
from typing import Iterator


class TapeWriter:
    def __init__(self, path: str):
        self._path = path
        self._fp = open(path, "w", encoding="utf8")

    def write(self, event: dict) -> None:
        json.dump(event, self._fp)
        self._fp.write("\n")
        self._fp.flush()

    def close(self):
        self._fp.close()


class TapeReader:
    def __init__(self, path: str):
        self._path = path

    def __iter__(self) -> Iterator[dict]:
        with open(self._path, "r", encoding="utf8") as fp:
            for line in fp:
                if not line.strip():
                    continue
                yield json.loads(line)


