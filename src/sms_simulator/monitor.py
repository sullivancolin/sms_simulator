import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ray.util.queue import Queue
from rich.live import Live
from rich.table import Table
from watchfiles import Change, DefaultFilter, watch

from sms_simulator.models import SMSResult, SMSStatus


class AddedFile(DefaultFilter):
    def __call__(self, change: Change, path: str) -> bool:
        return super().__call__(change, path) and change == Change.added


@dataclass()
class RowData:
    refresh_count: int = 0
    queue_size: int = 0
    sent_count: int = 0
    failed_count: int = 0
    failure_rate: float = 0.0
    throughput_avg: float = 0.0
    latencies: float = 0.0

    def to_table_row(self) -> tuple[str, str, str, str, str, str, str]:
        return (
            f"{self.refresh_count}",
            f"{self.queue_size}",
            f"{self.sent_count}",
            f"[red]{self.failed_count}",
            f"[red]{self.failed_count / self.sent_count if self.sent_count else 0.0:.2f} errs/sent",
            f"{self.throughput_avg:.2f} messages/second",
            f"{self.latencies/self.sent_count if self.sent_count else 0.0} ms/msg",
        )


def generate_table(row_data: RowData = RowData()) -> Table:
    table = Table()
    table.add_column("Number of Refreshes")
    table.add_column("Queue Size")
    table.add_column("Sent Messages")
    table.add_column("Failed Messages")
    table.add_column("Failure Rate")
    table.add_column("Throughput (msgs/sec)")
    table.add_column("Average latency (ms)")
    table.add_row(*row_data.to_table_row())
    return table


def monitor_results(source_dir: Path, interval: float) -> None:
    prev_time = None
    queue = Queue(
        maxsize=1000,
        actor_options={
            "name": "inbox",
            "namespace": "sms",
            "lifetime": "detached",
            "get_if_exists": True,
        },
    )
    row_data = RowData(0, queue.qsize(), 0, 0, 0.0, 0.0, 0.0)
    with Live(generate_table(row_data), refresh_per_second=interval) as live:
        for changes in watch(
            str(source_dir), watch_filter=AddedFile(), step=int(interval * 1000)
        ):
            start_time = prev_time if prev_time else datetime.now()
            batch_count = 0
            for _, filename in changes:
                if not Path(filename).exists():
                    continue
                with open(filename) as f:
                    sms = SMSResult(**json.load(f))

                row_data.sent_count += 1
                batch_count += 1
                row_data.latencies += sms.latency
                if sms.status == SMSStatus.FAILED:
                    row_data.failed_count += 1
                Path(filename).unlink()
            prev_time = datetime.now()
            row_data.throughput_avg = (
                batch_count / (prev_time - start_time).total_seconds()
            )
            row_data.refresh_count += 1
            row_data.queue_size = queue.qsize()
            live.update(generate_table(row_data))
