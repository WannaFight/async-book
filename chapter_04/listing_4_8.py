import aiohttp
import asyncio

from chapter_04 import fetch_status
from util import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "https://example.com", delay=1),
            fetch_status(session, "https://example.com", delay=10),
            fetch_status(session, "https://example.com", delay=10),
        ]
        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                print(await done_task)
            except asyncio.exceptions.TimeoutError:
                print("timeout!")

        for task in asyncio.tasks.all_tasks():
            print(task)


asyncio.run(main())
