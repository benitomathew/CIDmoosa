import shlex
from rich.console import Console
console = Console()
def show_help() :
    console.print("brief // exit // ")
    pass
def main():
    console.print("[bold yellow]CID MOOSA // CASE INVESTIGATION TERMINAL[/bold yellow]")
    console.print("Type [bold green]help[/bold green] to view available commands.\n")

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
                # Placeholder for Milestone 2
                console.print("[yellow]Case briefing will be loaded from JSON in Milestone 2.[/yellow]")
            else:
                console.print(f"[red]Unknown command:[/red] '{command}'. Type [bold]help[/bold] for options.")

        except ValueError as e:
            console.print(f"[red]Input error:[/red] {e}")
        except KeyboardInterrupt:

            console.print("\n[dim]Session interrupted. Exiting...[/dim]")
            break

if __name__ == "__main__":
    main()