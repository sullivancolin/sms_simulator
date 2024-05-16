"""Tests for the generate module."""

from pathlib import Path

from sms_simulator.generate import (
    enqueue_messages,
    get_n_messages,
    random_message,
    random_phone_number,
)
from sms_simulator.models import SMS


def test_random_phone_number() -> None:
    """Test the random_phone_number function."""
    phone_number = random_phone_number()
    assert isinstance(phone_number, int)
    assert len(str(phone_number)) == 10


def test_random_message() -> None:
    """Test the random_message function."""
    message = random_message()
    assert isinstance(message, str)
    assert 1 <= len(message) <= 100


def test_get_n_messages() -> None:
    """Test the get_n_messages function."""
    messages = list(get_n_messages(10))
    assert all(isinstance(message, SMS) for message in messages)
    assert len(messages) == 10


def test_dump_messages(tmp_path: Path) -> None:
    """Test the enqueue_messages function."""
    messages = get_n_messages(10)
    enqueue_messages(messages, tmp_path)
    assert len(list(tmp_path.iterdir())) == 10
