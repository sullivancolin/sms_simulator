import json
import random
import time
from dataclasses import asdict
from pathlib import Path

from watchfiles import watch

from sms_simulator.models import SMS, AddedFile, SMSResult, SMSStatus


def send_sms_messages(
    source_dir: Path,
    destination: Path,
    num_workers: int,
    latency_mean: int,
    failure_rate: float,
) -> None:
    for changes in watch(source_dir, watch_filter=AddedFile()):
        for _, name in changes:
            with open(name) as f:
                sms = SMS(**json.load(f))
            if random.random() < failure_rate:
                status = SMSStatus.FAILED
            else:
                status = SMSStatus.SUCCESS
            latency = max(0, random.gauss(latency_mean, latency_mean / 2))
            time.sleep(latency / 1000)
            result = SMSResult(sms.phone_number, sms.message, status, latency)
            with open(destination / Path(name).name, "w") as f:
                json.dump(asdict(result), f)
