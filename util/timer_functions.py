import time
from functools import wraps


def async_timed():
    def async_timed_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(f"starting `{func.__name__}` with args {args} and kwargs {kwargs}")
            start = time.monotonic()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.monotonic()
                total = end - start
                print(f"finished `{func.__name__}` in {total:.4f} second(s)")

        return wrapper

    return async_timed_decorator
