import pytest
from hcvss import (
    __app_name__,
    __version__,
    cli,
    hcvss
)
from typer.testing import CliRunner

runner = CliRunner()


class TestHCVSS:
    def test_version(self):
        result = runner.invoke(cli.app, ["--version"])
        assert result.exit_code == 0
        assert f"{__app_name__} v{__version__}\n" in result.stdout

    def test_check_command(self):
        # Test the 'check' command
        result = runner.invoke(cli.app, ['check'])
        assert result.exit_code == 0
        assert "Secret test2 is too short: 5 characters" in result.output

    def test_fetch_command(self):
        # Test the 'fetch' command
        result = runner.invoke(cli.app, ['fetch'])
        assert result.exit_code == 0
        assert "Step1" in result.output
