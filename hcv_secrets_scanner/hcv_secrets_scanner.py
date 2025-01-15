import typer

# Create a Typer app instance
app = typer.Typer()

# Define a command for the CLI
@app.command()
def hello(name: str):
    """Say hello to someone."""
    typer.echo(f"Hello, {name}!")

# Define another command
@app.command()
def goodbye(name: str, formal: bool = False):
    """Say goodbye to someone, with an option for formality."""
    if formal:
        typer.echo(f"Goodbye, Mr./Ms. {name}.")
    else:
        typer.echo(f"See you later, {name}!")

# Main block to run the app
if __name__ == "__main__":
    app()
