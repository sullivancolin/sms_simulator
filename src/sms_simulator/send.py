"""Spawn Processes to Send SMS Messages"""

import json
import random
import time
from dataclasses import asdict
from pathlib import Path

import ray
from ray.util.queue import Empty, Queue

from sms_simulator.models import SMS, SMSResult, SMSStatus


def send_message(
    source_path: str, target_dir: Path, latency: int, failure_rate: float
) -> None:
    """Send an SMS message.

    Args:
        source_path: The path to the source file containing the SMS message.
        target_dir: The directory to write the result file to.
        latency: The mean latency in milliseconds for sending the SMS message.
        failure_rate: The rate of failure for sending the SMS message.
    """
    with open(source_path) as f:
        sms = SMS(**json.load(f))
    if random.random() < failure_rate:
        status = SMSStatus.FAILED
    else:
        status = SMSStatus.SUCCESS
    latency = int(max(0, random.gauss(latency)))
    time.sleep(latency / 1000)
    result = SMSResult(sms.phone_number, sms.message, status, latency)
    with open(target_dir / Path(source_path).name, "w") as f:
        json.dump(asdict(result), f)
    Path(source_path).unlink()


@ray.remote
class SMSSender:
    """Actor class to send SMS messages from the queue in it's own process."""

    def __init__(
        self, inbox: Queue, target_dir: Path, latency_mean: int, failure_rate: float
    ):
        """Initialize the SMSSender actor.

        Args:
            inbox: A queue of source file paths containing SMS messages.
            target_dir: The directory to write the result files to.
            latency_mean: The mean latency in milliseconds for sending the SMS message.
            failure_rate: The rate of failure for sending the SMS message.
        """
        self.inbox = inbox
        self.target_dir = target_dir
        self.latency_mean = latency_mean
        self.failure_rate = failure_rate

    def send_messages(self) -> None:
        """Send SMS messages from the inbox queue."""
        while True:
            try:
                source_path = self.inbox.get(timeout=1)
            except Empty:
                continue
            send_message(
                source_path, self.target_dir, self.latency_mean, self.failure_rate
            )


def spawn_sms_senders(
    destination: Path,
    num_workers: int,
    latency_mean: int,
    failure_rate: float,
    inbox: Queue | None = None,
) -> None:
    """Spawn background SMS worker actors to pull SMS messages from the inbox queue and send them to the output destination.

    Args:
        destination: The directory to write the result files to.
        num_workers: The number of worker actors to spawn.
        latency_mean: The mean latency in milliseconds for sending the SMS message.
        failure_rate: The rate of failure for sending the SMS message.
    """
    if not inbox:
        inbox = Queue(
            maxsize=1000,
            actor_options={
                "name": "inbox",
                "namespace": "sms",
                "lifetime": "detached",
                "get_if_exists": True,
            },
        )
    actors = [
        SMSSender.options(  # type: ignore
            name=f"Actor ID: {num}",
            namespace="sms",
            lifetime="detached",
            get_if_exists=True,
        ).remote(inbox, destination, latency_mean, failure_rate)
        for num in range(num_workers)
    ]
    for actor in actors:
        actor.send_messages.remote()
