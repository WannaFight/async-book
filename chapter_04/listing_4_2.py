import asyncio
import aiohttp
from aiohttp import ClientSession

from util import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str, *, delay: int = 0) -> int:
    """Return status code of given url."""
    await asyncio.sleep(delay)
    async with session.get(url) as response:
        return response.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.example.com"
        status = await fetch_status(session, url)
        print(f"status for {url} is {status}")


# import asyncio
# asyncio.run(main())
