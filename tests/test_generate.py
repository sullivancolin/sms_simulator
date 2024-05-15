from pathlib import Path

from sms_simulator.generate import enqueue_messages, get_n_messages


def test_get_n_messages() -> None:
    messages = get_n_messages(10)
    assert sum(1 for _ in messages) == 10


def test_dump_messages(tmp_path: Path) -> None:
    messages = get_n_messages(10)
    enqueue_messages(messages, tmp_path)
    assert len(list(tmp_path.iterdir())) == 10
