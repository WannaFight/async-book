import asyncio

from util import delay


async def main():
    results = await asyncio.gather(delay(3), delay(1))
    # same order as passing -> [3, 1]. even though delay(1) will complete first
    print(results)


asyncio.run(main())
