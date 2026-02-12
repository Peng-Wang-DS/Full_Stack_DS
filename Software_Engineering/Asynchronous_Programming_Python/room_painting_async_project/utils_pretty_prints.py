RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"

STATE_LABEL = {
    "W1": "waiting first coat",
    "P1": "painting first coat",
    "D1": "drying",
    "W2": "waiting second coat",
    "P2": "painting second coat",
    "DN": "done",
}

STATE_COLOR = {
    "W1": CYAN,
    "P1": YELLOW,
    "D1": BLUE,
    "W2": CYAN,
    "P2": MAGENTA,
    "DN": GREEN,
}


def clear_screen():
    print("\033[2J\033[H", end="")


def make_progress_bar(percent, width=26):
    """Progress bar with a moving worker icon."""
    pct = max(0, min(100, int(percent)))
    pos = int((pct / 100) * (width - 1))
    chars = ["-"] * width

    for i in range(pos):
        chars[i] = "="

    if pct >= 100:
        chars[-1] = "#"
    else:
        # Draw a tiny "human" icon as o/
        chars[pos] = "o"
        if pos + 1 < width:
            chars[pos + 1] = "/"

    return "[" + "".join(chars) + "]"


def print_room_table(snapshot, completed, total_rooms, bar_width=26, thread_info=""):
    """Render one frame of the room status table."""
    clear_screen()
    print(f"{BOLD}ROOM PAINT ANIMATION{RESET}")
    print("=" * 80)
    if thread_info:
        print(f"Thread: {thread_info}")
        print("-" * 80)
    print(f"{'Room':<8}{'Progress':<34}{'Dry Left':<12}{'State'}")
    print("-" * 80)

    for room, state_key, percent, dry_left in snapshot:
        color = STATE_COLOR[state_key]
        dry_text = f"{dry_left:>5.1f}s" if state_key == "D1" else "   -"
        bar = make_progress_bar(percent, bar_width)
        label = STATE_LABEL[state_key]
        print(f"{color}{room:<8}{bar:<34}{dry_text:<12}{label}{RESET}")

    print("-" * 80)
    print(f"Completed: {completed}/{total_rooms}")
