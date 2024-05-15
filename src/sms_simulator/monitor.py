import json
from datetime import datetime
from pathlib import Path

from rich.live import Live
from rich.table import Table
from watchfiles import watch

from sms_simulator.models import AddedFile, SMSResult, SMSStatus


def generate_table(
    row_data: tuple[str, str, str] = (
        "0",
        "0",
        "[red]0",
        "[red]0.0 errs/sent",
        "0.0 msgs/sec",
        "0.0 ms/msg",
    ),
) -> Table:
    table = Table()
    table.add_column("Number of Refreshes")
    table.add_column("Sent Messages")
    table.add_column("Failed Messages")
    table.add_column("Failure Rate")
    table.add_column("Throughput (msgs/sec)")
    table.add_column("Average latency (ms)")
    table.add_row(*row_data)
    return table


def monitor_results(source_dir: Path, interval: int) -> None:
    sent_count = 0
    failed_count = 0
    refresh_count = 0
    latencies = 0
    with Live(generate_table(), refresh_per_second=interval) as live:
        for changes in watch(
            str(source_dir), watch_filter=AddedFile(), step=interval * 1000
        ):
            start_time = datetime.now()
            batch_count = 0
            refresh_count += 1
            for _, filename in changes:
                if not Path(filename).exists():
                    continue
                with open(filename) as f:
                    sms = SMSResult(**json.load(f))

                sent_count += 1
                batch_count += 1
                latencies += sms.latency
                if sms.status == SMSStatus.FAILED:
                    failed_count += 1
                Path(filename).unlink()

                row_data = (
                    f"{refresh_count}",
                    f"{sent_count}",
                    f"[red]{failed_count}",
                    f"[red]{failed_count / sent_count:.2f} errs/sent",
                    f"{batch_count / (datetime.now() - start_time).total_seconds():.2f} messages/second",
                    f"{latencies/sent_count} ms/msg",
                )
            live.update(generate_table(row_data))
