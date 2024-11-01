import asyncio
import aiohttp

from chapter_04 import fetch_status
from util import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:  # good
        urls = ["https://example.com", "python://example.com"]
        tasks = [fetch_status(session, url) for url in urls]
        codes = await asyncio.gather(*tasks, return_exceptions=True)
        print(codes)


asyncio.run(main())
