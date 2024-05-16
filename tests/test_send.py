"""Test the send module."""

import json
import time
from pathlib import Path
from typing import Any

import pytest

from sms_simulator.send import Queue, SMSSender, send_message, spawn_sms_senders


@pytest.fixture
def sms_json() -> dict[str, Any]:
    return {"phone_number": 1234567890, "message": "Hello, World!"}


@pytest.fixture
def source_path(tmp_path: Path) -> Path:
    """Return a source file path."""
    source_path = tmp_path / "source.json"
    return source_path


@pytest.fixture()
def target_dir(tmp_path: Path) -> Path:
    """Return a target directory."""
    target_dir = tmp_path / "target"
    return target_dir


def test_send_message(
    source_path: Path, target_dir: Path, sms_json: dict[str, Any]
) -> None:
    """Test the send_message function."""
    with open(source_path, "w") as f:
        json.dump(sms_json, f)
    target_dir.mkdir()
    send_message(str(source_path), target_dir, 500, 0.5)
    assert len(list(target_dir.iterdir())) == 1
    with open(target_dir / source_path.name) as f:
        sms_result = json.load(f)
    assert sms_json["phone_number"] == sms_result["phone_number"]
    assert sms_json["message"] == sms_result["message"]
    assert sms_result["status"] in {"success", "failed"}
    assert sms_result["latency"] >= 0.0


def test_spawn_sms_senders(
    source_path: Path, target_dir: Path, sms_json: dict[str, Any]
) -> None:
    """Test the spawn_sms_senders function."""

    inbox = Queue(
        maxsize=1000,
        actor_options={
            "name": "inbox",
            "namespace": "sms",
            "lifetime": "detached",
            "get_if_exists": True,
        },
    )
    with open(source_path, "w") as f:
        json.dump(sms_json, f)

    inbox.put(str(source_path))
    target_dir.mkdir()
    spawn_sms_senders(target_dir, 1, 500, 0.5)
    time.sleep(1)
    assert len(list(target_dir.iterdir())) == 1


def test_sms_sender(
    source_path: Path, target_dir: Path, sms_json: dict[str, Any]
) -> None:
    """Test the SMSSender actor class."""
    inbox = Queue(
        maxsize=1000,
        actor_options={
            "name": "inbox",
            "namespace": "sms",
            "lifetime": "detached",
            "get_if_exists": True,
        },
    )
    with open(source_path, "w") as f:
        json.dump(sms_json, f)

    inbox.put(str(source_path))
    target_dir.mkdir()
    LocalSMSSender = SMSSender.__dict__["__ray_metadata__"].__dict__["modified_class"]
    sender = LocalSMSSender(inbox, target_dir, 500, 0.5)
    assert hasattr(sender, "send_messages")
