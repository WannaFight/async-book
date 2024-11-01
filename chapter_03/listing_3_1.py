"""
Simple echo server with mutliple clients support.
!!! THIS SHIT IS USING 100% !!!
"""

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ("127.0.0.1", 8000)
server_socket.bind(server_address)
server_socket.setblocking(False)
server_socket.listen()
print(f"listening on {server_address}...")

conns = []

try:
    while True:
        try:
            conn, client_addr = server_socket.accept()
            conn.setblocking(False)
            print(f"I got a connection from {client_addr}")
            conns.append(conn)
        except BlockingIOError:
            pass

        for conn in conns:
            buffer = b""
            buf_size = 2

            try:
                while buffer[-buf_size:] != b"\r\n":
                    data = conn.recv(buf_size)
                    if not data:
                        break
                    print(f"I got data: {data}")
                    buffer += data

                print(f"All the data is: {buffer}")
                conn.sendall(b"echo from socket: " + buffer)
            except ConnectionResetError:
                conns.remove(conn)
            except BlockingIOError:
                pass
finally:
    server_socket.close()
