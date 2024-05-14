import json
from pathlib import Path

from rich.progress import Progress
from watchfiles import watch

from sms_simulator.models import AddedFile, SMSResult, SMSStatus


def monitor_results(source_dir: Path, interval: int) -> None:
    with Progress() as progress:
        sent_count = progress.add_task("Watching messages...", total=None)
        failed_count = progress.add_task("Failed messages...", total=None)
        for changes in watch(
            source_dir, watch_filter=AddedFile(), step=int(1000 * interval)
        ):
            for _, path in changes:
                with open(path) as f:
                    sms = SMSResult(**json.load(f))
                progress.update(sent_count, advance=1)
                if sms.status == SMSStatus.FAILED:
                    progress.update(failed_count, advance=1)
                # path.unlink()
