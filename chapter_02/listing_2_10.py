import asyncio

from util import delay


async def main():
    wait_time = 2
    task = asyncio.create_task(delay(3))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), timeout=wait_time)
        print(result)
    except asyncio.TimeoutError:
        print(f"task took longer than {wait_time} seconds")
        print(f"was the task cancelled? {task.cancelled()}")
        result = await task
        print(result)


asyncio.run(main())
