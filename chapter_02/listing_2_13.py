import asyncio

from util import async_timed, delay as _delay


@async_timed()
async def delay(seconds: int) -> int:
    await _delay(seconds)


@async_timed()
async def main():
    # # total time: 5 seconds
    # await asyncio.create_task(delay(2))
    # await asyncio.create_task(delay(3))

    # # total time: 2 seconds
    # t1, t2 = asyncio.create_task(delay(2)), asyncio.create_task(delay(3))
    # await t1, t2

    # total time: 3 seconds
    t1, t2 = asyncio.create_task(delay(2)), asyncio.create_task(delay(3))
    await t1
    await t2


asyncio.run(main())
