import shlex
import json
from ui import show_briefing , show_suspects , show_clue , show_room
from rich.console import Console
console = Console()
def show_help() :
    console.print("[bold cyan]brief[/bold cyan] - View case summary | [bold cyan]suspects[/bold cyan] - View suspects & alibis | [bold cyan]exit[/bold cyan] - Quit ")
    pass
def main():
    console.print("[bold yellow]CID MOOSA // CASE INVESTIGATION TERMINAL[/bold yellow]")
    console.print("Type [bold green]help[/bold green] to view available commands.\n")
    with open("case_data.json", "r", encoding="utf-8") as f:
        case_data = json.load(f)    
    while True:
        try:

            raw_input = console.input("[bold cyan]cid-moosa>[/bold cyan] ").strip()
            
            if not raw_input:
                continue

            parts = shlex.split(raw_input)
            command = parts[0].lower()
            args = parts[1:]

            if command == "exit" or command == "quit":
                console.print("[dim]Closing investigation terminal...[/dim]")
                break
            elif command == "help":
                show_help()
            elif command == "brief":
                show_briefing(case_data)
            elif command == "suspects":
                show_suspects(case_data["suspects"])     
            else:
                console.print(f"[red]Unknown command:[/red] '{command}'. Type [bold]help[/bold] for options.")

        except ValueError as e:
            console.print(f"[red]Input error:[/red] {e}")
        except KeyboardInterrupt:

            console.print("\n[dim]Session interrupted. Exiting...[/dim]")
            break

if __name__ == "__main__":
    main()