import asyncio

from util import async_timed, delay


@async_timed()  # total ~9 sec
async def bad_cycle():
    delay_times = [3, 3, 3]
    [await asyncio.create_task(delay(seconds)) for seconds in delay_times]
    # ^ problem is here. on first loop of list compr. awaiting task as soon as its being created


@async_timed()  # total ~3 sec
async def good_cycle():
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]


@async_timed()
async def better_practice():
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    await asyncio.gather(*tasks)


async def main() -> None:
    await bad_cycle()
    await good_cycle()
    await better_practice()


asyncio.run(main())
