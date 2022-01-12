import asyncio
import click

from server import AsyncServer
from logger import set_logger


@click.command()
@click.option('--local', help='host:port')
@click.option('--remote', help='host:port')
@click.option('--level', default="INFO")
@click.option('--log_file', default=None)
def run(local, remote, level, log_file=None):
    set_logger(level, log_file)

    async_server = AsyncServer(tuple(local.split(":")), tuple(remote.split(":")))

    try:
        asyncio.get_event_loop().run_until_complete(async_server.start())
    except RuntimeError:
        asyncio.run(async_server.start())
