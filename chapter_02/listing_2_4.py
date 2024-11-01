import asyncio
import time

from util import delay


async def add_one(number: int) -> int:
    await delay(1)
    return number + 1


async def hello() -> str:
    await delay(1)
    return "Hello world"


async def main() -> None:
    start = time.time()
    message = await hello()
    number = await add_one(1)
    print(message)
    print(number)
    print(f"{time.time() - start:.4f} elapsed")  # ~2 sec


asyncio.run(main())
