import asyncio


async def main():
    print("started")
    await asyncio.sleep(1)
    print("done")


loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
finally:
    loop.close()
