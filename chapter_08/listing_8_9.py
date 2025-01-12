from collections import deque
from typing import Awaitable, Callable


class MessageStore:
    def __init__(self, callback: Callable[[deque], Awaitable[None]], max_size: int):
        self._deque = deque(maxlen=max_size)
        self._callback = callback

    async def append(self, item):
        self._deque.append(item)
        await self._callback(self._deque)
