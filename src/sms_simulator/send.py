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
    with open(source_path) as f:
        sms = SMS(**json.load(f))
    if random.random() < failure_rate:
        status = SMSStatus.FAILED
    else:
        status = SMSStatus.SUCCESS
    latency = int(max(0, random.gauss(latency, latency / 2)))
    time.sleep(latency / 1000)
    result = SMSResult(sms.phone_number, sms.message, status, latency)
    with open(target_dir / Path(source_path).name, "w") as f:
        json.dump(asdict(result), f)
    Path(source_path).unlink()


@ray.remote
class SMSWorker:
    def __init__(
        self, inbox: Queue, target_dir: Path, latency_mean: int, failure_rate: float
    ):
        self.inbox = inbox
        self.target_dir = target_dir
        self.latency_mean = latency_mean
        self.failure_rate = failure_rate

    def send_messages(self) -> None:
        while True:
            try:
                source_path = self.inbox.get(timeout=1)
            except Empty:
                continue
            send_message(
                source_path, self.target_dir, self.latency_mean, self.failure_rate
            )


def send_sms_messages(
    destination: Path,
    num_workers: int,
    latency_mean: int,
    failure_rate: float,
) -> None:
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
        SMSWorker.options(
            name=f"Actor ID: {num}", namespace="sms", lifetime="detached"
        ).remote(inbox, destination, latency_mean, failure_rate)
        for num in range(num_workers)
    ]
    for actor in actors:
        actor.send_messages.remote()
