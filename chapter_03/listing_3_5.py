import asyncio
import logging
import signal
import socket

echo_tasks = []
loop = asyncio.new_event_loop()


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def echo(conn: socket, loop: asyncio.AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(conn, 1024):
            if data == b"boom\r\n":
                raise Exception("unexpected network error")
            await loop.sock_sendall(conn, b"echo from server: " + data)
    except Exception:
        logging.exception("fatal error")
    finally:
        conn.close()


async def connection_listener(
    server_socket: socket, loop: asyncio.AbstractEventLoop
) -> None:
    while True:
        conn, addr = await loop.sock_accept(server_socket)
        conn.setblocking(False)
        print(f"Got connection from {addr}")
        echo_tasks.append(asyncio.create_task(echo(conn, loop)))


async def close_echo_tasks(echo_tasks: list[asyncio.Task]) -> None:
    """Note: this is not production ready solution! After SIGINT or SIGTERM is received,
    server socket is not closed for new incoming requests – thay won't be awaited!
    """
    for task in [asyncio.wait_for(task, 2) for task in echo_tasks]:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass


async def main():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ("127.0.0.1", 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    print(f"Listening on {server_address[0]}:{server_address[1]}...")

    for sig in signal.SIGINT, signal.SIGTERM:
        loop.add_signal_handler(sig, shutdown)

    await connection_listener(server_socket, loop)


try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
