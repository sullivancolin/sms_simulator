import pytest
from typer.testing import CliRunner

from sms_simulator.cli import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture for a CliRunner to invoke cli commands."""
    return CliRunner()


def test_cli_help(cli_runner: CliRunner) -> None:
    """Test cli help text."""
    result = cli_runner.invoke(app, ["--help"])
    assert "CLI interface for the sms service simulator." in result.output
