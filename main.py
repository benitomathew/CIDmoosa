import shlex
import json
from ui import show_briefing , show_suspects , show_clue , show_room
from rich.console import Console
from engine import (
    create_initial_state,
    look_around,
    move_room,
    inspect_clue,
    ask_suspect,
    show_notes,
    make_accusation,
)

console = Console()
def show_help():
    console.print(
        "[bold cyan]brief[/bold cyan] - Case summary | "
        "[bold cyan]look[/bold cyan] - Inspect current room | "
        "[bold cyan]go <room>[/bold cyan] - Move room\n"
        "[bold cyan]inspect <clue>[/bold cyan] - Examine evidence | "
        "[bold cyan]suspects[/bold cyan] - View dossier | "
        "[bold cyan]ask <suspect> [clue][/bold cyan] - Question suspect\n"
        "[bold cyan]notes[/bold cyan] - View collected evidence | "
        "[bold cyan]exit[/bold cyan] - Quit"
        "[bold cyan]accuse[/bold cyan] - To accuse a suspect"
    )
def main():

    console.print("[bold yellow]CID MOOSA // CASE INVESTIGATION TERMINAL[/bold yellow]")
    console.print("Type [bold green]help[/bold green] to view available commands.\n")
    with open("case_data.json", "r", encoding="utf-8") as f:
        case_data = json.load(f)    
    state = create_initial_state(case_data)
    show_briefing(case_data)
    look_around(state, case_data)    
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
            elif command == "look":
                look_around(state, case_data)
            elif command == "go":
                if not args:
                    console.print("[yellow]Usage: go <room_id>[/yellow]")
                else:
                    move_room(state, case_data, args[0].lower())
            elif command == "inspect":
                if not args:
                    console.print("[yellow]Usage: inspect <clue_id>[/yellow]")
                else:
                    inspect_clue(state, case_data, args[0].lower())
            elif command == "ask":
                if not args:
                    console.print("[yellow]Usage: ask <suspect_id> [optional_clue_id][/yellow]")
                else:
                    suspect_id = args[0].lower()
                    clue_id = args[1].lower() if len(args) > 1 else None
                    ask_suspect(state, case_data, suspect_id, clue_id)
            elif command == "notes":
                show_notes(state, case_data)
            elif command == "accuse":
                make_accusation(state, case_data)    
            else:
                console.print(f"[red]Unknown command:[/red] '{command}'. Type [bold]help[/bold] for options.")
            if state.get("game_over"):
                console.print("\n[bold yellow]Thanks for playing CID MOOSA![/bold yellow]")
                break
        except ValueError as e:
            console.print(f"[red]Input error:[/red] {e}")
        except KeyboardInterrupt:

            console.print("\n[dim]Session interrupted. Exiting...[/dim]")
            break

if __name__ == "__main__":
    main()