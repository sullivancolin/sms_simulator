"""Module to generate random SMS messages and enqueue them in the inbox."""

import json
import random
import string
from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

from sms_simulator.models import SMS
from sms_simulator.send import Queue

numbers = list(range(0, 9))


def random_phone_number() -> int:
    """Generate a random phone number.

    Returns:
        A random phone number as an integer.
    """
    return int(str("".join(str(num) for num in random.choices(numbers, k=10))))


def random_message() -> str:
    """Generate a random message string.

    Returns:
        A random message string.
    """
    return "".join(random.choices(string.ascii_letters, k=random.randint(1, 100)))


def get_n_messages(n: int = 1000) -> Iterable[SMS]:
    """Generate n random SMS messages.

    Args:
        n: The number of messages to generate.

    Returns:
        An iterable of SMS messages.

    """
    return (
        SMS(
            random_phone_number(),
            random_message(),
        )
        for _ in range(n)
    )


def enqueue_messages(messages: Iterable[SMS], path: Path) -> None:
    """Enqueue messages in the inbox, and write them to destination path.

    Args:
        messages: An iterable of SMS messages.
        path: The destination path to write the messages to.
    """
    inbox = Queue(
        maxsize=1000,
        actor_options={
            "name": "inbox",
            "namespace": "sms",
            "lifetime": "detached",
            "get_if_exists": True,
        },
    )
    for message in messages:
        filename = path / (uuid4().hex + ".json")
        with open(filename, "w") as f:
            json.dump(asdict(message), f)
        inbox.put(filename)
