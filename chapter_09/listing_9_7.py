import asyncio

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute


class UserCounter(WebSocketEndpoint):
    encoding = "text"
    sockets = []

    async def on_connect(self, websocket):
        await websocket.accept()
        self.sockets.append(websocket)
        await self._send_count()

    async def on_disconnect(self, websocket, close_code):
        self.sockets.remove(websocket)
        await self._send_count()

    async def on_receive(self, websocket, data):
        pass

    async def _send_count(self):
        if len(self.sockets) <= 0:
            return
        count_str = str(len(self.sockets))
        task_to_socket = {
            asyncio.create_task(websocket.send_text(count_str)): websocket
            for websocket in self.sockets
        }

        done, pending = await asyncio.wait(task_to_socket)
        for task in done:
            if task.exception() is not None:
                if task_to_socket[task] in self.sockets:
                    self.sockets.remove(task_to_socket[task])


app = Starlette(routes=[WebSocketRoute("/counter", UserCounter)])
