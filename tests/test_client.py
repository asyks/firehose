from unittest import TestCase
from unittest.mock import MagicMock, patch

from spigot.client import Client


class TestClientConstructor(TestCase):
    @patch("spigot.client.Connection")
    def test_instantiates_connection_object(
        self, mock_connection_init: MagicMock
    ) -> None:
        assert Client(
            hostname="foobar",
            port=80,
        ).connection
        assert mock_connection_init.called
