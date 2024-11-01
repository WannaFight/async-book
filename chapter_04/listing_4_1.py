import asyncio
import socket
from types import TracebackType
from typing import Type


class ConnectedSocket:
    def __init__(self, server_socket: socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self) -> socket:
        print("entering context manager, waiting for connections...")
        loop = asyncio.get_event_loop()
        conn, addr = await loop.sock_accept(self._server_socket)
        self._connection = conn
        print("accepted a connection")
        return self._connection

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        print("exiting context manager")
        self._connection.close()
        print("closed connection")


async def main():
    loop = asyncio.get_event_loop()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ("127.0.0.1", 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    print("listening on", server_address)

    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(data)


asyncio.run(main())
