import shutil
import sys


def save_cursor_pos():
    sys.stdout.write("\0337")


def restore_cursor_pos():
    sys.stdout.write("\0338")


def move_to_top():
    sys.stdout.write("\033[H")


def move_to_bottom() -> int:
    _, total_rows = shutil.get_terminal_size()
    input_row = total_rows - 1
    sys.stdout.write(f"\033[{input_row}E")
    return total_rows


def delete_line():
    sys.stdout.write("\033[2K")


def clear_line():
    sys.stdout.write("\033[2K\033[0G")


def move_back():
    sys.stdout.write("\033[1D")
