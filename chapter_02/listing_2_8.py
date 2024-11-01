import asyncio

from util import delay


async def main():
    long_task = asyncio.create_task(delay(4))

    seconds_elapsed = 0

    while not long_task.done():
        print("task is running, checking again in a second")
        await asyncio.sleep(1)
        seconds_elapsed += 1
        if seconds_elapsed == 5:
            long_task.cancel()  # can only be catched at await statement

    try:
        print("inside try before await")
        print(await long_task)
        print("inside try after await")
    except asyncio.CancelledError:
        print("our task was cancelled")


asyncio.run(main())
