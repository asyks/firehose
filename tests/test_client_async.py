from asyncio import StreamReader, StreamWriter
from unittest.mock import AsyncMock, Mock, patch

import pytest

from spigot.client import Client
from spigot.types import MessageType
from spigot.response import Response


@pytest.mark.asyncio
@patch("spigot.client.Client.send_message", return_type=AsyncMock)
class TestClientRunConcurrently:
    async def test_run_concurrently_single_message(
        self, mock_client_send_message: AsyncMock
    ) -> None:
        client = Client(
            hostname="foobar",
            port=80,
            message_type=MessageType.HTTP,
            number_of_messages=1,
        )
        await client.run_concurrently()

        assert mock_client_send_message.call_count == 1

    async def test_run_concurrently_multi_message(
        self, mock_client_send_message: AsyncMock
    ) -> None:
        client = Client(
            hostname="foobar",
            port=80,
            message_type=MessageType.HTTP,
            number_of_messages=5,
        )
        await client.run_concurrently()

        assert mock_client_send_message.call_count == 5


@pytest.mark.asyncio
class TestClientSendMessage:
    @patch("spigot.connection.Connection.close", return_type=AsyncMock)
    @patch("spigot.connection.Connection.open", return_type=AsyncMock)
    @patch("spigot.connection.Connection.send", return_type=AsyncMock)
    async def test_calls_internal_connection_interface(
        self,
        mock_connection_send: AsyncMock,
        mock_connection_open: AsyncMock,
        mock_connection_close: AsyncMock,
    ) -> None:
        TEST_MESSAGE = "test message"
        mock_connection_send.return_value = Mock(
            spec=Response, content_str=TEST_MESSAGE
        )

        client = Client(
            hostname="foobar",
            port=80,
            message_type=MessageType.HTTP,
            number_of_messages=5,
        )
        response = await client.send_message(sequence_num=1)

        assert response.content_str == TEST_MESSAGE
        assert mock_connection_open.await_count == 1
        assert mock_connection_send.await_count == 1
        assert mock_connection_close.call_count == 1

    @patch("spigot.connection.open_connection", return_type=AsyncMock)
    async def test_collects_response_data(
        self,
        mock_asyncio_open_connection: AsyncMock,
    ) -> None:
        response_data = b'some arbirary response data'
        mock_stream_reader = AsyncMock(
            spec=StreamReader,
            readline=AsyncMock(
                side_effect=[
                    response_data, ''
                ]
            )
        )
        mock_asyncio_open_connection.return_value = (
            mock_stream_reader, Mock(spec=StreamWriter)
        )

        client = Client(
            hostname="foobar",
            port=80,
            message_type=MessageType.HTTP,
            number_of_messages=5,
        )
        response = await client.send_message(sequence_num=1)

        assert response.content_bytes == response_data
