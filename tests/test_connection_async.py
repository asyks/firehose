from asyncio import StreamReader, StreamWriter
from unittest.mock import AsyncMock, Mock, patch

import pytest

from firehose.connection import Connection


@pytest.mark.asyncio
@patch("firehose.connection.open_connection", return_type=AsyncMock)
class TestConnectionOpen:
    async def test_calls_asyncio_open_connection(
        self, mock_asyncio_open_connection: AsyncMock
    ) -> None:
        mock_asyncio_open_connection.return_value = (
            Mock(spec=StreamReader), Mock(spec=StreamWriter)
        )
        connection = Connection(hostname="foobar", port=80)

        await connection.open()

        assert mock_asyncio_open_connection.call_count == 1
