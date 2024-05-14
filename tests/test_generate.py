from pathlib import Path

from sms_simulator.generate import dump_messages, get_n_messages


def test_get_n_messages() -> None:
    messages = get_n_messages(10)
    assert len(messages) == 10


def test_dump_messages(tmp_path: Path) -> None:
    messages = get_n_messages(10)
    dump_messages(messages, tmp_path)
    assert len(list(tmp_path.iterdir())) == 10
