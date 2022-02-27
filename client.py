import asyncio
from asyncio import StreamReader
from email.parser import BytesHeaderParser
from http.client import HTTPMessage, BadStatusLine


async def send_get_request():
    # /v1/bpi/currentprice.json
    # api.coindesk.com
    message = "GET / HTTP/1.1\r\n" "Host: 127.0.0.1\r\n" "accept: */*\r\n" "\r\n"

    print("CONNECTION OPEN")
    reader, writer = await asyncio.open_connection("127.0.0.1", 8000)

    print(f"SEND: {message!r}")
    writer.write(message.encode())

    while True:
        line = await reader.readline()
        if not line:
            break

        print(line.decode())

    print("CONNECTION CLOSE")
    writer.close()


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    print(f"Send: {message!r}")
    writer.write(message.encode())

    data = await reader.read(100)
    print(f"Received: {data.decode()!r}")

    print("Close the connection")
    writer.close()


async def main():
    """
    await asyncio.gather(
        *(tcp_echo_client(f'Hello World {i}!') for i in range(10))
    )
    """
    await asyncio.gather(*(send_get_request() for i in range(30)))


asyncio.run(main())
