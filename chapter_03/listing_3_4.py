import asyncio
import signal

from util import delay


def cancel_tasks():
    print("got SIGINT")
    tasks = asyncio.all_tasks()
    print(f"cancelling {len(tasks)} task(s).")

    for task in tasks:
        task.cancel()


async def main():
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)  # graceful shutdown
    await delay(10)


asyncio.run(main())
