import asyncio
from util import delay
from util.timer_functions import async_timed


async def pos_int_async(until: int):
    for num in range(until):
        await delay(num)
        yield num


@async_timed()
async def main():
    async_gen = pos_int_async(3)
    print(type(async_gen))
    async for number in async_gen:
        print(f"Got number {number}")


asyncio.run(main())
