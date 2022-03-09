from io import StringIO
from unittest.mock import Mock

import pytest

from firehose.client import Client
from firehose.types import MessageType, Response


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_client_send_message")
class TestClientRunConcurrently:
    async def test_run_concurrently_single_message(
        self, mock_client_send_message: pytest.fixture
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
        self, mock_client_send_message: pytest.fixture
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
@pytest.mark.usefixtures(
    "mock_connection_close", "mock_connection_open", "mock_connection_send"
)
class TestClientSendMessage:
    async def test_send_message(
        self,
        mock_connection_close: pytest.fixture,
        mock_connection_open: pytest.fixture,
        mock_connection_send: pytest.fixture,
    ) -> None:
        TEST_MESSAGE = "test message"
        client = Client(
            hostname="foobar",
            port=80,
            message_type=MessageType.HTTP,
            number_of_messages=5,
        )
        mock_connection_send.return_value = Mock(
            spec=Response, data=StringIO(TEST_MESSAGE)
        )

        response = await client.send_message(sequence_num=1)

        assert response.data.readline() == TEST_MESSAGE
        assert mock_connection_open.await_count == 1
        assert mock_connection_send.await_count == 1
        assert mock_connection_close.call_count == 1
