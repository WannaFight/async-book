import asyncio
import logging


class ServerState:
    def __init__(self):
        self._writers: list[asyncio.StreamWriter] = []

    async def add_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        self._writers.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    async def _on_connect(self, writer: asyncio.StreamWriter):
        writer.write(f"Welcome! {len(self._writers)} users are online!\n".encode())
        await writer.drain()
        await self._notify_all("New user connected!\n")

    async def _echo(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            while (data := await reader.readline()) != b"":
                writer.write(data)
                await writer.drain()
            self._writers.remove(writer)
            await self._notify_all(
                f"Client disconected. {len(self._writers)} user(s) are online!\n"
            )
        except Exception:
            logging.exception("error reading from client")
            self._writers.remove(writer)

    async def _notify_all(self, msg: str):
        msg = msg.encode()
        for writer in self._writers:
            try:
                writer.write(msg)
                await writer.drain()
            except ConnectionError:
                logging.exception("could not write to client")
                self._writers.remove(writer)


async def main():
    server_state = ServerState()

    async def client_connected(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        await server_state.add_client(reader, writer)

    server = await asyncio.start_server(client_connected, "127.0.0.1", 8000)

    async with server:
        await server.serve_forever()


asyncio.run(main())
