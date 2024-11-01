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
    message = asyncio.create_task(hello())
    number = asyncio.create_task(add_one(1))
    print(type(message))
    print(type(number))
    print(await message)
    print(await number)
    print(f"{time.time() - start:.4f} elapsed")  # ~1 sec


asyncio.run(main())
