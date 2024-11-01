import asyncio

from util import async_timed, delay


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100_000_000):
        counter += i
    return counter


@async_timed()
async def main():
    """
    Total time: cpu_bound_work().time + cpu_bound_work().time + delay(3).time ~ 7 sec
    """
    await asyncio.gather(
        asyncio.create_task(cpu_bound_work()),
        asyncio.create_task(cpu_bound_work()),
        delay(3),
    )


asyncio.run(main())
