import typer

from sms_simulator import __version__

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
def generate() -> None:
    """Generate SMS messages."""
    typer.echo("Generating SMS messages.")


@app.command()
def send() -> None:
    """Send SMS messages."""
    typer.echo("Sending SMS messages.")


@app.command()
def monitor() -> None:
    """Monitor SMS progress."""
    typer.echo("Monitoring SMS messages.")


if __name__ == "__main__":
    app()
