from unittest import TestCase
from unittest.mock import MagicMock, patch

from spigot.client import Client


class TestClient(TestCase):
    @patch("spigot.client.Connection")
    def test_get_connection(self, mock_connection_init: MagicMock) -> None:
        client = Client(
            hostname="foobar",
            port=80,
        )
        client._get_connection()
        assert mock_connection_init.called
