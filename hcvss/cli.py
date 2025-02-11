"""This module provides the Hashivault Secrets Scanner CLI."""

from typing import Optional

import typer

from hcvss import __app_name__, __version__
from .hcvss import SecretsScanner

app = typer.Typer()


@app.command()
def check(
    filename: str = typer.Option(
        "test_secrets.json",
        "--file",
        "-f",
        help="The secrets file to check"
    )
) -> None:
    """Check the secrets in the file."""
    hcvss = SecretsScanner()
    hcvss.check_secrets(filename)


@app.command()
def fetch(
    filename: str = typer.Option(
        "test_secrets.json",
        "--file",
        "-f",
        help="The secrets file to check"
    )
) -> None:
    """Fetch the secrets from HCP."""
    hcvss = SecretsScanner()
    hcvss.fetch_hcp_secrets(filename)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
