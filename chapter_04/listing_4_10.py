import asyncio
import aiohttp

from chapter_04 import fetch_status
from util import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://example.com"
        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, delay=3)),
        ]
        done, pending = await asyncio.wait(fetchers, timeout=1)
        print(f"Done tasks counts: {len(done)}")  # 2
        print(f"Pending tasks counts: {len(pending)}")  # 1

        for done_task in done:
            print(await done_task)

        for pending_task in pending:
            pending_task.cancel()


asyncio.run(main())
