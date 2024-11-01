import asyncio
import logging
import socket
from asyncio import AbstractEventLoop

tasks = []


async def echo(conn: socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(conn, 1024):
            if data == b"boom\r\n":
                raise Exception("unexpected network error")
            await loop.sock_sendall(conn, b"echo from server: " + data)
    except Exception:
        logging.exception("fatal error")
    finally:
        conn.close()  # close client connection so it won't sent any data


async def listen_for_connection(server_sock: socket, loop: AbstractEventLoop) -> None:
    while True:
        conn, addr = await loop.sock_accept(server_sock)
        conn.setblocking(False)
        print(f"Got connections from {addr}")
        asyncio.create_task(echo(conn, loop))


async def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_addr = ("127.0.0.1", 8000)
    server_sock.setblocking(False)
    server_sock.bind(server_addr)
    server_sock.listen()
    print(f"Listening on {server_addr[0]}:{server_addr[1]}...")

    await listen_for_connection(server_sock, asyncio.get_event_loop())


asyncio.run(main())
