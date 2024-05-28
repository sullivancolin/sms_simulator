"""Spawn Processes to Send SMS Messages"""

from pathlib import Path
from threading import Thread

from ray import serve
from ray.util.queue import Empty, Queue

from sms_simulator.send import send_message


@serve.deployment
class SMSSenderDeployment:
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
        self.sender_thread = Thread(target=self.send_messages)
        self.sender_thread.start()

    def send_messages(self) -> None:
        """Send SMS messages from the inbox queue."""
        print("starting to sent messages")
        while True:
            try:
                source_path = self.inbox.get(timeout=1)
            except Empty:
                continue
            send_message(
                source_path, self.target_dir, self.latency_mean, self.failure_rate
            )

    def stop(self) -> None:
        """Stop the SMSSender actor."""
        self.sender_thread.join()


def spawn_sms_serve_deployment(
    destination: Path,
    num_workers: int,
    latency_mean: int,
    failure_rate: float,
    inbox: Queue | None = None,
) -> None:
    """Spawn ray serve SMS sender replicas to pull SMS messages from the inbox queue and send them to the output destination.

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

    sms_deployment = SMSSenderDeployment.options(  # type: ignore
        num_replicas=num_workers
    ).bind(
        inbox=inbox,
        target_dir=destination,
        latency_mean=latency_mean,
        failure_rate=failure_rate,
    )
    serve.run(
        sms_deployment,
        name="sms_deployment",
    )
