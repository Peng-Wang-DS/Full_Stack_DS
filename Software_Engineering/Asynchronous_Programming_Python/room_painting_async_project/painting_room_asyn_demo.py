import asyncio
import threading
import time

from utils_pretty_prints import GREEN, print_room_table, RESET


# Simulation settings
ROOMS = ["A", "B", "C", "D", "E", "F"]
PAINT_SECONDS = 2.0
DRY_SECONDS = 3.0
FRAME_SECONDS = 0.10
BAR_WIDTH = 26

# Shared live state
room_state = {room: "W1" for room in ROOMS}
room_progress = {room: 0 for room in ROOMS}
room_dry_left = {room: 0.0 for room in ROOMS}
done_count = 0
last_to_thread_worker = "not used yet"
lock = asyncio.Lock()


async def set_room(room, *, state=None, progress=None, dry_left=None):
    """Atomically update tracked fields for one room."""
    async with lock:
        if state is not None:
            room_state[room] = state
        if progress is not None:
            room_progress[room] = progress
        if dry_left is not None:
            room_dry_left[room] = dry_left


async def run_timer(total_seconds, on_tick):
    """Run a frame-based timer and call `on_tick(elapsed)` each frame."""
    start = time.perf_counter()
    while True:
        elapsed = time.perf_counter() - start
        await on_tick(elapsed)
        if elapsed >= total_seconds:
            break
        await asyncio.sleep(FRAME_SECONDS)

async def paint_room(room, coat_number):
    """Animate one paint coat for a room."""
    global last_to_thread_worker
    state_key = "P1" if coat_number == 1 else "P2"
    await set_room(room, state=state_key, progress=0)
    # Probe a real worker thread so thread usage is visible in the UI.
    worker_thread = await asyncio.to_thread(
        lambda: f"{threading.current_thread().name} (id={threading.current_thread().ident})"
    )
    async with lock:
        last_to_thread_worker = worker_thread

    async def on_tick(elapsed):
        pct = min(100, int((elapsed / PAINT_SECONDS) * 100))
        await set_room(room, progress=pct)

    await run_timer(PAINT_SECONDS, on_tick)


async def dry_room(room, queue):
    """Animate drying, then re-queue room for second coat."""
    await set_room(room, state="D1", progress=0)

    async def on_tick(elapsed):
        left = max(0.0, DRY_SECONDS - elapsed)
        await set_room(room, dry_left=left)

    await run_timer(DRY_SECONDS, on_tick)
    await set_room(room, state="W2", dry_left=0.0)
    await queue.put((room, 2))


async def worker_paint_room(queue):
    """Consume paint jobs from queue until all rooms are done."""
    global done_count
    total_rooms = len(ROOMS)

    while done_count < total_rooms:
        room, coat_number = await queue.get()
        try:
            await paint_room(room, coat_number)

            if coat_number == 1:
                asyncio.create_task(dry_room(room, queue))
            else:
                async with lock:
                    room_state[room] = "DN"
                    room_progress[room] = 100
                    done_count += 1
        finally:
            queue.task_done()


async def monitor_progress():
    """Render the live status table until completion."""
    while True:
        async with lock:
            snapshot = [(r, room_state[r], room_progress[r], room_dry_left[r]) for r in ROOMS]
            completed = done_count
            worker_thread = last_to_thread_worker

        current = threading.current_thread()
        thread_info = (
            f"event_loop={current.name} (id={current.ident}) | "
            f"to_thread={worker_thread}"
        )
        print_room_table(
            snapshot,
            completed,
            len(ROOMS),
            bar_width=BAR_WIDTH,
            thread_info=thread_info,
        )

        if completed >= len(ROOMS):
            break
        await asyncio.sleep(FRAME_SECONDS)

async def main():
    """Set up queue, run worker/renderer tasks, and await completion."""
    queue = asyncio.Queue()

    for room in ROOMS:
        await queue.put((room, 1))

    worker_task = asyncio.create_task(worker_paint_room(queue))
    renderer_task = asyncio.create_task(monitor_progress())

    await worker_task
    await queue.join()
    await renderer_task

    print(f"\n{GREEN}All rooms are fully painted.{RESET}")


if __name__ == "__main__":
    asyncio.run(main())
