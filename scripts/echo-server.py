import argparse
import asyncio
from asyncio import StreamReader, StreamWriter
from email.utils import formatdate
from enum import Enum
from random import randrange
from time import time
from typing import Callable


class MessageType(Enum):
    HTTP = "http"
    RAW = "raw"


DESCRIPTION = "Concurrently recieve and echo network requests."
PORT_HELP = "Port to which to bind the server (default 8888)."
TYPE_HELP = (
    "Type of message to send back to the client: 'raw' or 'http' (default 'http')."
)

DEFAULT_TYPE = MessageType.HTTP.value
DEFAULT_PORT = 8888
LOCALHOST = "127.0.0.1"

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("--port", type=int, help=PORT_HELP, default=DEFAULT_PORT)
parser.add_argument(
    "--type",
    type=str,
    help=TYPE_HELP,
    choices=(MessageType.HTTP.value, MessageType.RAW.value),
    default=DEFAULT_TYPE,
)


def _construct_http_message(message: str) -> bytes:
    status_code = 200
    status_text = "OK"
    timestamp = formatdate(time())
    status_line = f"HTTP/1.1 {status_code} {status_text}"
    headers = f"Date: {timestamp}"

    return "\n".join((status_line, headers, message)).encode()


async def echo_http(reader: StreamReader, writer: StreamWriter) -> None:
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info("peername")

    print(f"Received {message!r} from {addr!r}")

    await asyncio.sleep(randrange(0, 3))

    print(f"Send: {message!r}")

    # Contruct http bytes, and send it back to the client
    response = _construct_http_message(message)
    writer.write(response)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def echo_raw(reader: StreamReader, writer: StreamWriter) -> None:
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info("peername")

    print(f"Received {message!r} from {addr!r}")

    await asyncio.sleep(randrange(0, 3))

    print(f"Send: {message!r}")

    # Send the raw bytes back to the client
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def start_server(client_connected_coroutine: Callable, port: int) -> None:
    server = await asyncio.start_server(client_connected_coroutine, LOCALHOST, port)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)  # type: ignore [union-attr]
    print(f"Serving on {addrs} ...")

    async with server:
        await server.serve_forever()


def cmd() -> None:
    args = parser.parse_args()

    if args.type == MessageType.HTTP.value:
        client_connected_coroutine = echo_http
    else:
        client_connected_coroutine = echo_raw

    asyncio.run(start_server(client_connected_coroutine, args.port))


if __name__ == "__main__":
    cmd()
