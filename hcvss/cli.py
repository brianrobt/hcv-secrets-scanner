"""This module provides the Hashivault Secrets Scanner CLI."""

from typing import Optional

import typer

from hcvss import __app_name__, __version__, hcvss

app = typer.Typer()


@app.command()
def check() -> None:
    """Check the secrets in the file."""
    hcvss.check_secrets('test_secrets.json')


@app.command()
def fetch() -> None:
    """Fetch the secrets from HCP."""
    hcvss.fetch_hcp_secrets()


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
