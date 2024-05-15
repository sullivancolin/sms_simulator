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
    return int(str("".join(str(num) for num in random.choices(numbers, k=10))))


def random_message() -> str:
    return "".join(random.choices(string.ascii_letters, k=random.randint(1, 100)))


def get_n_messages(n: int = 1000) -> Iterable[SMS]:
    return (
        SMS(
            random_phone_number(),
            random_message(),
        )
        for _ in range(n)
    )


def enqueue_messages(messages: Iterable[SMS], path: Path) -> None:
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
