from multiprocessing import cpu_count
from pathlib import Path
from typing import Annotated

import typer

from sms_simulator import __version__
from sms_simulator.generate import dump_messages, get_n_messages
from sms_simulator.monitor import monitor_results
from sms_simulator.send import send_sms_messages

app = typer.Typer(help="CLI interface for the sms service simulator.")


def version_callback(value: bool) -> None:
    if value:
        print(f"{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Print the current version.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    return


@app.command()
def generate(
    n: Annotated[
        int, typer.Argument(help="Number of sms messages to generate.")
    ] = 1000,
    target_dir: Annotated[
        str, typer.Option(help="Directory to write messages.")
    ] = "inbox",
) -> None:
    """Generate SMS messages."""
    messages = get_n_messages(n)
    dump_messages(messages, Path(target_dir))
    typer.echo(f"Generated {n} messages at {target_dir}.")


@app.command()
def send(
    source_dir: Annotated[
        str, typer.Argument(help="directory to watch for new messagse to send")
    ] = "inbox",
    dest_dir: Annotated[
        str, typer.Argument(help="directory to write success/failre messages")
    ] = "outbox",
    num_workers: Annotated[
        int, typer.Option(help="Number of workers to send messages.")
    ] = cpu_count() - 1,
    latency_mean: Annotated[
        int, typer.Option(help="Mean latency in milliseconds.")
    ] = 250,
    failure_rate: Annotated[
        float, typer.Option(help="Rate of failure in sending messages.")
    ] = 0.1,
) -> None:
    """Send SMS messages."""
    send_sms_messages(
        Path(source_dir),
        Path(dest_dir),
        num_workers,
        latency_mean,
        failure_rate,
    )


@app.command()
def monitor(
    target_dir: Annotated[
        str, typer.Argument(help="directory to watch for sms results")
    ] = "outbox",
    interval: Annotated[int, typer.Option(help="Interval in seconds.")] = 1,
) -> None:
    """Monitor SMS progress."""
    monitor_results(Path(target_dir), interval=interval)


if __name__ == "__main__":
    app()
