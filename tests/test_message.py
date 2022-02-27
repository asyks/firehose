from unittest import TestCase

from firehose.constants import DEFAULT_HTTP_VERSION
from firehose.message import HttpMessage


class HttpMessageTestCase(TestCase):
    def test_default_version(self) -> None:
        assert (
            HttpMessage(hostname="foobar", path="/some/path").version
            == DEFAULT_HTTP_VERSION
        )

    def test_provided_version(self) -> None:
        provided_http_version = "HTTP/1.0"
        assert (
            HttpMessage(
                hostname="foobar", path="/some/path", version=provided_http_version
            ).version
            == provided_http_version
        )
