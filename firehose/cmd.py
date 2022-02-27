import asyncio
import argparse
from urllib.parse import urlparse

from .client import Client
from .types import MessageType


DESCRIPTION = "Send up to 50 async concurrent network requests to the target."
URL_HELP = "URL of the target resource (including: domain, port, and path)."
TYPE_HELP = "Type of message to send: 'raw' or 'http' (default 'http')."
MSG_HELP = "(For type 'raw' messages only) the message text to be sent."
REQS_HELP = "Number of requests to send to the target (maximum 50, default 5)."

DEFAULT_TYPE = MessageType.HTTP.value
DEFAULT_REQS = 5
DEFAULT_MSG = ""
DEFAULT_SCHEME = "http"


parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("url", metavar="U", type=str, help=URL_HELP)
parser.add_argument(
    "--type",
    type=str,
    help=TYPE_HELP,
    choices=(MessageType.HTTP.value, MessageType.RAW.value),
    default=DEFAULT_TYPE,
)
parser.add_argument("--reqs", type=int, help=REQS_HELP, default=DEFAULT_REQS)
parser.add_argument("--msg", type=str, help=MSG_HELP, required=False)


def get_default_port(scheme: str) -> int:
    return 443 if scheme == "https" else 80


def cmd() -> None:
    args = parser.parse_args()

    if args.type == MessageType.HTTP.value:
        message_type = MessageType.HTTP
        url = urlparse(args.url, scheme=DEFAULT_SCHEME)
        hostname = url.hostname or ""
        port = int(url.port) if url.port else get_default_port(url.scheme)
        path = url.path

    if args.type == MessageType.RAW.value:
        message_type = MessageType.RAW
        hostname, port_str = args.url.split(":")
        port = int(port_str) if port_str else get_default_port("")
        path = ""

    client = Client(
        hostname=hostname,
        port=port,
        path=path,
        message_type=message_type,
        number_of_messages=args.reqs or DEFAULT_REQS,
        message_data=args.msg or DEFAULT_MSG,
    )
    asyncio.run(client.run_concurrently())
