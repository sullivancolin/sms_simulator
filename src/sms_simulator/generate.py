import json
import random
import string
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

from sms_simulator.models import SMS


def random_phone_number() -> int:
    return int(
        str("".join(str(num) for num in random.choices(list(range(0, 9)), k=10)))
    )


def random_message() -> str:
    return "".join(random.choices(string.ascii_letters, k=random.randint(10, 100)))


def get_n_messages(n: int = 1000) -> list[SMS]:
    return [
        SMS(
            random_phone_number(),
            random_message(),
        )
        for _ in range(n)
    ]


def dump_messages(messages: list[SMS], path: Path) -> None:
    for message in messages:
        with open(path / (uuid4().hex + ".json"), "w") as f:
            json.dump(asdict(message), f)


if __name__ == "__main__":
    messages = get_n_messages(10)
    print(messages)
