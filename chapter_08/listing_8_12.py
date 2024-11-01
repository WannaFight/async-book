import asyncio
import logging


class ChatServer:
    def __init__(self):
        self._username_to_writer: dict[str, asyncio.StreamWriter] = {}

    async def start_chat_server(self, host: str, port: int):
        server = await asyncio.start_server(self.client_connected, host, port)

        async with server:
            await server.serve_forever()

    async def client_connected(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        command = await reader.readline()
        print(f"CONNECTED {reader} {writer}")
        command, args = command.split(b" ")
        if command == b"CONNECT":
            username = args.replace(b"\n", b"").decode()
            self._add_user(username, reader, writer)
            await self._on_conect(username, writer)
        else:
            logging.error("Got invalid command from client, disconnecting...")
            writer.close()
            await writer.wait_closed()

    def _add_user(
        self, username: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        self._username_to_writer[username] = writer
        asyncio.create_task(self._listen_for_messages(username, reader))

    async def _on_connect(self, username: str):
        pass
