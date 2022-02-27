from unittest import TestCase

from firehose.client import Client
from firehose.constants import DEFAULT_MESSAGE, DEFAULT_PATH
from firehose.types import MessageType


class ClientTestCase(TestCase):
    def test_init_default_values(self) -> None:
        client = Client(
            hostname="foobar",
            port=80,
            message_type=MessageType.HTTP,
            number_of_messages=5,
        )

        assert client.path == DEFAULT_PATH
        assert client.message_data == DEFAULT_MESSAGE

    def test_init_provided_values(self) -> None:
        provided_path = "/some/path"
        provided_message = "an arbitrary message"

        client = Client(
            hostname="foobar",
            port=80,
            message_type=MessageType.HTTP,
            number_of_messages=5,
            path=provided_path,
            message_data=provided_message,
        )

        assert client.path == provided_path
        assert client.message_data == provided_message
