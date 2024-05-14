from dataclasses import dataclass
from enum import Enum

from watchfiles import Change, DefaultFilter


class AddedFile(DefaultFilter):
    def __call__(self, change: Change, path: str) -> bool:
        return super().__call__(change, path) and change == Change.added


class SMSStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class SMS:
    phone_number: int
    message: str


@dataclass(frozen=True, slots=True)
class SMSResult:
    phone_number: int
    message: str
    status: SMSStatus
    latency: int
