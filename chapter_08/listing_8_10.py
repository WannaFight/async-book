import asyncio
import os
import sys
import tty
from collections import deque

from chapter_08.listing_8_5 import create_stdin_reader
from chapter_08.listing_8_7 import (
    delete_line,
    move_to_bottom,
    move_to_top,
    restore_cursor_pos,
    save_cursor_pos,
)
from chapter_08.listing_8_8 import read_line
from chapter_08.listing_8_9 import MessageStore


async def sleep(delay: int, store: MessageStore):
    await store.append(f"Starting delay {delay}")
    await asyncio.sleep(delay)
    await store.append(f"Finished delay {delay}")


async def main():
    tty.setcbreak(sys.stdin)
    os.system("clear")
    rows = move_to_bottom()

    async def redraw_output(items: deque):
        save_cursor_pos()
        move_to_top()
        for item in items:
            delete_line()
            print(item)
        restore_cursor_pos()

    messages = MessageStore(redraw_output, rows - 1)
    stdin_reader = await create_stdin_reader()

    while True:
        line = await read_line(stdin_reader)
        delay_time = int(line)
        asyncio.create_task(sleep(delay_time, messages))


asyncio.run(main())
