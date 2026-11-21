from rich.console import Console
from rich.panel import Panel
from ui import show_room, show_clue

console = Console()

def create_initial_state(case_data: dict) -> dict:
    return {
        "current_room": case_data["starting_room"],
        "collected_clues": [],
    }

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
    
    pass

def inspect_clue(state: dict, case_data: dict, clue_id: str):
    current_room_id = state["current_room"]
    room_clues = case_data["rooms"][current_room_id]["clues"]
    if clue_id in room_clues:
        clue_data  = case_data["clues"][clue_id]
        show_clue(clue_id, clue_data)
        if clue_id not in state["collected_clues"]:
            state["collected_clues"].append(clue_id)
    else:
         console.print("[yellow] clue isint in this room")    


    # TODO: Check if `clue_id` is in `room_clues`.
    # If yes:
    #   1. Get clue_data = case_data["clues"][clue_id]
    #   2. Call show_clue(clue_id, clue_data)
    #   3. If clue_id is not already in state["collected_clues"], append it!
    # If no: print a yellow message telling the player that clue isn't in this room.
    pass

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