from dataclasses import dataclass


@dataclass
class Response():
    status: int
    json: dict