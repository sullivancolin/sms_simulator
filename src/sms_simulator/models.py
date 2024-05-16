"""Module defining the data models used in the SMS simulator."""

from dataclasses import dataclass
from enum import Enum


class SMSStatus(str, Enum):
    """Enum of possible SMS statuses.

    `SMSStatus.SUCCESS`: The SMS was successfully sent.
    `SMSStatusFAILED`: The SMS failed to send.
    """

    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class SMS:
    """Data class representing an SMS message."""

    phone_number: int
    message: str


@dataclass(frozen=True, slots=True)
class SMSResult:
    """Data class representing the result of sending an SMS message."""

    phone_number: int
    message: str
    status: SMSStatus
    latency: int
