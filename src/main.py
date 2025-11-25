import typer
from rich.console import Console

from src.logging.logger_handler import LevelName, LoggerHandler
from src.models.settings.create_schema import create_database_schema

logger_handler = LoggerHandler(level=LevelName.DEBUG)
logger = logger_handler.get_logger()

app = typer.Typer()
console = Console()

db_app = typer.Typer(help="Database management commands.")
app.add_typer(db_app, name="db")


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


@db_app.command("create")
def create_database():
    console.print("[bold yellow]Creating database schema...[/]")

    try:
        create_database_schema()
        console.print("[bold green]✔ Database schema created successfully.[/]")
    except Exception as exc:
        logger.error("Error creating database schema: %s", exc)
        console.print(
            "[bold red]❌ Error creating database schema[/]\n"
            "• Verify that MySQL is installed\n"
            "• Ensure it is running on port 3306\n"
            "• Confirm username and password in the configuration file"
        )


if __name__ == "__main__":
    app()
