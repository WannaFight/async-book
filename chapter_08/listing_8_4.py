import asyncio

from util import delay


async def main():
    """Endless inputing numbers, with no launchin tasks."""
    while True:
        delay_time = input("number:")
        asyncio.create_task(delay(int(delay_time)))


asyncio.run(main())
