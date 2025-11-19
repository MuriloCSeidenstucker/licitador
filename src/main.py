import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def hello(name: str = "mundo"):
    console.print(f"[bold green]Olá, [bold red]{name}[bold green]![/]")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        console.print(
            f"[bold green]Goodbye Ms. [bold red]{name}[bold green]. Have a good day."
        )
    else:
        console.print(f"[bold green]Bye [bold red]{name}[bold green]!")


if __name__ == "__main__":
    app()
