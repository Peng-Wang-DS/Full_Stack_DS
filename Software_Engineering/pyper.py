from pyper import task
import asyncio


async def some_task1():
    await asyncio.sleep(10)
    print("running task 1")
    return "task1_completed"


async def some_task2(x):
    print(x)
    await asyncio.sleep(10)
    print("running task 2")
    return "task2_completed"


async def some_task3(x):
    print(x)
    await asyncio.sleep(10)
    print("running task 3")
    return "task3_completed"


pipe = task(some_task1) | task(some_task2) | task(some_task3)


if __name__ == "__main__":
    for output in pipe():
        print(output)
