import asyncio
from unittest.mock import Mock, AsyncMock

import pytest
from pytest_mock import mocker


@pytest.fixture(scope="function")
def mock_connection_open(mocker: mocker) -> AsyncMock:
    async_mock = AsyncMock(return_value=None)
    mocker.patch("firehose.connection.Connection.open", side_effect=async_mock)

    return async_mock


@pytest.fixture(scope="function")
def mock_connection_close(mocker: mocker) -> Mock:
    mock = Mock(return_value=None)
    mocker.patch("firehose.connection.Connection.close", side_effect=mock)

    return mock


@pytest.fixture(scope="function")
def mock_connection_send(mocker: mocker) -> asyncio.Future:
    async_mock = AsyncMock()
    mocker.patch("firehose.connection.Connection.send", side_effect=async_mock)

    return async_mock


@pytest.fixture(scope="function")
def mock_client_send_message(mocker: mocker) -> asyncio.Future:
    async_mock = AsyncMock()
    mocker.patch("firehose.client.Client.send_message", side_effect=async_mock)

    return async_mock
