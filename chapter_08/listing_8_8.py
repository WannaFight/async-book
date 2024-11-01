import asyncio
from collections import deque
import sys

from chapter_08.listing_8_7 import clear_line, move_back


async def read_line(stdin_reader: asyncio.StreamReader) -> str:
    def erase_last_char():
        move_back()
        sys.stdout.write(" ")
        move_back()

    delete_char = b"\x7f"
    input_bufer = deque()

    while (input_char := await stdin_reader.read(1)) != b"\n":
        if input_char == delete_char:
            input_bufer.pop()
            erase_last_char()
            sys.stdout.flush()
        else:
            input_bufer.append(input_char)
            sys.stdout.write(input_char.decode())
            sys.stdout.flush()

    clear_line()
    return b"".join(input_bufer).decode()
