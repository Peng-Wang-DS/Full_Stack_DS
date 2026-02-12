import asyncio
import os
import sys


# Avoid importing local `pyper.py` in this folder.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if p not in ("", CURRENT_DIR)]

from pyper import task

async def some_task1():
    print("running task 1")
    await asyncio.sleep(2)

    return "task1_completed"


async def some_task2(x):
    print(x)
    print("running task 2")
    await asyncio.sleep(2)

    return "task2_completed"


async def some_task3(x):
    print(x)
    print("running task 3")
    await asyncio.sleep(2)

    return "task3_completed"


pipe = task(some_task1) | task(some_task2) | task(some_task3)


async def run_pipeline():
    async for output in pipe():
        print(output)

async def main():
    x = await some_task1()
    y = await some_task2(x)
    await some_task3(y)

if __name__ == "__main__":
    # asyncio.run(run_pipeline())
    asyncio.run(run_pipeline())
