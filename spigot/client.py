from __future__ import annotations

from asyncio import gather

from .connection import Connection
from .constants import DEFAULT_MESSAGE, DEFAULT_PATH
from .exceptions import ClientInitError
from .message import HttpMessage
from .types import MessageType, Response


class Client:
    def __init__(
        self,
        hostname: str,
        port: int,
        message_type: MessageType,
        number_of_messages: int,
        path: str = DEFAULT_PATH,
        message_data: str = DEFAULT_MESSAGE,
    ) -> None:
        super().__init__()
        if message_type is MessageType.HTTP:
            if path is None:
                raise ClientInitError("Path is required to send HTTP messages")

        self.message_type = message_type
        self.number_of_messages = number_of_messages
        self.hostname = hostname
        self.port = port
        self.path = path
        self.message_data = message_data

    @property
    def message(self) -> HttpMessage | str:
        if self.message_type is MessageType.HTTP:
            return HttpMessage(self.hostname, self.path)

        if self.message_type is MessageType.RAW:
            return self.message_data

        return self.message_data

    async def send_message(self, sequence_num: int) -> Response:
        connection = Connection(self.hostname, self.port)
        await connection.open()
        print(f"Sending message {sequence_num}: {self.message}")
        response = await connection.send(str(self.message))
        print(f"Recieved response {sequence_num}, closing connection")
        connection.close()

        return response

    async def run_concurrently(self) -> None:
        await gather(
            *(self.send_message(n + 1) for n in range(self.number_of_messages))
        )
