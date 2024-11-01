import asyncio

from util import async_timed

import httpx
import requests


@async_timed()
async def get_example_status() -> int:
    return requests.get("http://example.com").status_code


@async_timed()
async def aget_example_status() -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get("http://example.com")
    return response.status_code


@async_timed()
async def main():
    """
    Total time: request1.time + resuest2.time + request3.time ~ 0.9 sec
    """
    await asyncio.gather(
        asyncio.create_task(get_example_status()),
        asyncio.create_task(get_example_status()),
        asyncio.create_task(get_example_status()),
    )

    await asyncio.gather(
        asyncio.create_task(aget_example_status()),
        asyncio.create_task(aget_example_status()),
        asyncio.create_task(aget_example_status()),
    )


asyncio.run(main())
