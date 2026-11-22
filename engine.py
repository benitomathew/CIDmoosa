from rich.console import Console
from rich.panel import Panel
from ui import show_room, show_clue

console = Console()

def create_initial_state(case_data: dict) -> dict:
    return {
        "current_room": case_data["starting_room"],
        "collected_clues": [],
        "action_points": 12,
        "game_over": False,
    }
def spend_action_point(state: dict) -> bool:
    if state["action_points"] <= 0:
        console.print("[bold red]Out of Action Points! Morning has arrived—you must type 'accuse' now.[/bold red]")
        return False
    state["action_points"] -= 1
    console.print(f"[dim](Action Points remaining: {state['action_points']})[/dim]")
    return True

def look_around(state: dict, case_data: dict):
    room_id = state["current_room"]
    room_data = case_data["rooms"][room_id]
    show_room(room_id, room_data)

def move_room(state: dict, case_data: dict, target_room: str):
    current_room_id = state["current_room"]
    valid_exits = case_data["rooms"][current_room_id]["exits"]
    if target_room in valid_exits:
        state["current_room"] = target_room
        look_around(state, case_data)
    else:
        console.print(f"[red]valid exits are {valid_exits}")    
    
    

def inspect_clue(state: dict, case_data: dict, clue_id: str):
    current_room_id = state["current_room"]
    room_clues = case_data["rooms"][current_room_id]["clues"]

    if clue_id not in room_clues:
        console.print(f"[yellow]No clue named '{clue_id}' found in this room.[/yellow]")
        return

    if clue_id not in state["collected_clues"]:
        if not spend_action_point(state):
            return
        state["collected_clues"].append(clue_id)

    clue_data = case_data["clues"][clue_id]
    show_clue(clue_id, clue_data)
   

def ask_suspect(state: dict, case_data: dict, suspect_id: str, clue_id: str = None):
    if suspect_id not in case_data["suspects"]:
        console.print(f"[red]Unknown suspect:[/red] '{suspect_id}'. Check [bold]suspects[/bold] for IDs.")
        return

    suspect = case_data["suspects"][suspect_id]

    # Case A: Player asks general follow-up (`ask dan`)
    if clue_id is None:
        panel = Panel(
            f"\"{suspect['follow_up']}\"",
            title=f"[bold yellow]{suspect['name']} (Follow-up)[/bold yellow]",
            border_style="yellow"
        )
        console.print(panel)
        return

    # Case B: Player confronts suspect with a clue (`ask dan git_reflog`)
    if clue_id not in state["collected_clues"]:
        console.print(f"[yellow]You haven't inspected '{clue_id}' yet! Inspect it before confronting a suspect.[/yellow]")
        return

    reactions = suspect.get("evidence_reactions", {})
    reply = reactions.get(clue_id, "They shrug. \"I don't know anything about that.\"")

    panel = Panel(
        f"\"{reply}\"",
        title=f"[bold magenta]{suspect['name']} on {clue_id}[/bold magenta]",
        border_style="magenta"
    )
    console.print(panel)
def show_notes(state: dict, case_data: dict):
    """Displays all clues the player has collected so far."""
    if not state["collected_clues"]:
        console.print("[dim]No clues collected yet. Use 'inspect <clue_id>' to gather evidence.[/dim]")
        return

    lines = []
    for cid in state["collected_clues"]:
        clue = case_data["clues"][cid]
        lines.append(f"• [bold cyan]{cid}[/bold cyan] ({clue['name']}): {clue['summary']}")

    panel = Panel(
        "\n".join(lines),
        title="[bold green]Investigation Notebook[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)    

def make_accusation(state: dict, case_data: dict):
    console.print("\n[bold yellow]--- FINAL ACCUSATION ---[/bold yellow]")
    console.print(f"Suspect IDs: {', '.join(case_data['suspects'].keys())}")

    accused = console.input("[bold cyan]Who tampered with bounties.db? (enter ID): [/bold cyan]").strip().lower()

    if accused not in case_data["suspects"]:
        console.print(f"[red]Invalid suspect ID '{accused}'. Accusation cancelled.[/red]")
        return

    solution = case_data["solution"]
    required = solution["required_evidence"]
    has_all_proof = all(clue in state["collected_clues"] for clue in required)

    if accused == solution["culprit"] and has_all_proof:
        panel = Panel(
            solution["closing_summary"],
            title="[bold green]CASE SOLVED — BOUNTY LEADERBOARD RESTORED[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
        console.print(panel)
        state["game_over"] = True

    elif accused == solution["culprit"] and not has_all_proof:
        missing = [c for c in required if c not in state["collected_clues"]]
        panel = Panel(
            f"You pointed the finger at {case_data['suspects'][accused]['name']}, and you're right—but without "
            f"hard evidence , they talked their way out of it before morning payouts ran.",
            title="[bold yellow]INSUFFICIENT EVIDENCE — CASE DISMISSED[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        console.print(panel)
        state["game_over"] = True

    else:
        accused_name = case_data["suspects"][accused]["name"]
        panel = Panel(
            f"You accused {accused_name}, triggering a heated argument in the lab. While everyone was distracted, "
            f"the real culprit wiped the remaining logs and walked away with the ₹5,000 bounty.",
            title="[bold red]WRONG ACCUSATION — CASE GONE COLD[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        console.print(panel)
        state["game_over"] = True    