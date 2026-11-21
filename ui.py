from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def show_briefing(case_data: dict):
    """Displays the opening case summary inside a yellow box."""
    panel = Panel(
        case_data["briefing"],
        title=f"[bold yellow]{case_data['title']}[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(panel)


def show_suspects(suspects: dict):
    """Displays all suspects and their alibis in a formatted table."""
    table = Table(title="Suspects Dossier", show_lines=True)
    table.add_column("ID", style="bold cyan", no_wrap=True)
    table.add_column("Name", style="bold white")
    table.add_column("Role", style="yellow")
    table.add_column("Stated Alibi", style="white")

    # Loop through the dictionary: suspect_id is "benito", info is the inner dict
    for suspect_id, info in suspects.items():
        table.add_row(suspect_id, info["name"], info["role"], info["alibi"])

    console.print(table)


def show_room(room_id: str, room_data: dict):
    """Displays the current room's description, clues to inspect, and exits."""
    # Join lists into readable strings, e.g. "sqlite_history, tmux_pane"
    clues_list = ", ".join(room_data["clues"]) if room_data["clues"] else "None"
    exits_list = ", ".join(room_data["exits"])

    body = (
        f"{room_data['description']}\n\n"
        f"[bold cyan]Clues here:[/bold cyan] {clues_list}\n"
        f"[bold green]Exits:[/bold green] {exits_list}"
    )

    # TODO: Create a Panel using `body`, title=f"[bold white]{room_data['name']}[/bold white]",
    # and border_style="blue", then print it with console.print(...)
    pass


def show_clue(clue_id: str, clue: dict):
    """Displays a clue's summary and raw terminal/log output."""
    content = f"[italic]{clue['summary']}[/italic]\n\n[white]{clue['raw_output']}[/white]"

    # TODO: Create a Panel using `content`, title=f"[bold cyan]{clue['name']} ({clue_id})[/bold cyan]",
    # and border_style="cyan", then print it with console.print(...)
    pass