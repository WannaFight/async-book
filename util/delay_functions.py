import asyncio


async def delay(seconds: int) -> int:
    print(f"sleeping for {seconds} sec...")
    await asyncio.sleep(seconds)
    print(f"finished sleeping for {seconds} sec")
    return seconds
