import asyncio

from util import delay


async def main():
    delay_task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(delay_task, timeout=5)
        print(result)
    except asyncio.TimeoutError:
        print("time out!")
        print(f"was the task cancelled? {delay_task.cancelled()}")


asyncio.run(main())
