import asyncio
import aiohttp
from chapter_04 import fetch_status
from util import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "https://example.com", delay=1),
            fetch_status(session, "https://example.com", delay=1),
            fetch_status(session, "https://example.com", delay=10),
        ]
        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task)


asyncio.run(main())
