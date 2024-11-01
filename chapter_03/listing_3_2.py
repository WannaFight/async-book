import selectors
import socket
from selectors import SelectorKey

selector = selectors.DefaultSelector()

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_addr = ("127.0.0.1", 8000)
server_socket.setblocking(False)
server_socket.bind(server_addr)
server_socket.listen()
print("listening on", server_addr)

selector.register(server_socket, selectors.EVENT_READ)

while True:
    events: list[tuple[SelectorKey, int]] = selector.select(timeout=1)

    if not events:
        print("no events, waiting a bit more...")

    for event, _ in events:
        event_socket: socket.socket = event.fileobj
        print(f"{event=}, {event_socket=}")

        if event_socket == server_socket:
            conn, addr = server_socket.accept()
            conn.setblocking(False)
            print(f"I got a connection from {addr}")
            selector.register(conn, selectors.EVENT_READ)
        else:
            data = event_socket.recv(1024)
            print(f"I got some data: {data}")
            event_socket.send(data)
