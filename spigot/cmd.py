"""
Command line interface for the spigot package.

The package can be run as a module, e.g.
```
python -m spigot http://127.0.0.1:8080 --type=http --reqs 10 --msg "an http message"
```
For more info on command line invocation of this package:
```
python -m spigot --help
```
"""
import asyncio
import argparse
from urllib.parse import urlparse

from spigot.constants import DEFAULT_PATH
from spigot.message import Message, HttpMessage, RawMessage

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


async def run_concurrently(
    client: Client,
    message: Message,
    count: int,
) -> None:
    async def send_sequenced_message(sequence_num: int) -> None:
        print(f"Sending message {sequence_num}: {str(message)}")
        await client.send_message(message)
        print(f"Recieved response {sequence_num}, closing connection")

    await asyncio.gather(*(send_sequenced_message(n + 1) for n in range(count)))


def cmd() -> None:
    args = parser.parse_args()

    message_data = args.msg or DEFAULT_MSG
    count = args.reqs or DEFAULT_REQS
    url = urlparse(args.url, scheme=DEFAULT_SCHEME)

    hostname = url.hostname or ""
    port = int(url.port) if url.port else get_default_port(url.scheme)
    path = url.path or DEFAULT_PATH

    message: Message
    if args.type == MessageType.HTTP.value:
        message = HttpMessage(hostname=hostname, path=path)
    else:
        message = RawMessage(data=message_data)

    client = Client(hostname=hostname, port=port)

    asyncio.run(run_concurrently(client, message, count))
