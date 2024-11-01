import asyncio
import logging
import aiohttp

from chapter_04 import fetch_status
from util import async_timed


@async_timed()
async def all_completed():
    """
    asyncio.ALL_COMPLETED - `pending` will be always zero, `done` - completed or tasks with exceptions
    """
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "https://example.com")),
            asyncio.create_task(fetch_status(session, "https://example.com")),
        ]
        done, pending = await asyncio.wait(fetchers)
        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            print(await done_task)


@async_timed()
async def handle_exc():
    """
    asyncio.ALL_COMPLETED - `pending` will be always zero, `done` - completed or tasks with exceptions
    """
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "https://example.com")),
            asyncio.create_task(fetch_status(session, "python://example.com")),
        ]
        done, pending = await asyncio.wait(fetchers)
        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("request got exception", exc_info=done_task.exception())


@async_timed()
async def first_exc():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, "ypthon://bad.com")),
            asyncio.create_task(
                fetch_status(session, "https://www.example.com", delay=3)
            ),
            asyncio.create_task(
                fetch_status(session, "https://www.example.com", delay=3)
            ),
        ]
        done, pending = await asyncio.wait(
            fetchers, return_when=asyncio.FIRST_EXCEPTION
        )
        print(f"Done task count: {len(done)}")
        print(f"Pending task count: {len(pending)}")

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("request error", exc_info=done_task.exception())

        for pending_task in pending:
            pending_task.cancel()


@async_timed()
async def first_completed():
    async with aiohttp.ClientSession() as session:
        url = "https://www.example.com"
        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]
        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )
            print(f"Done task count: {len(done)}")
            print(f"Pending task count: {len(pending)}")

            for done_task in done:
                print(await done_task)


async def main():
    # await all_completed()
    # await handle_exc()
    # await first_exc()
    await first_completed()


asyncio.run(main())
