import click
import asyncio

from server import AsyncServer
from logger import set_logger


@click.command()
@click.option("--local", default="0.0.0.0:5000")
@click.option("--remote")
@click.option("--level", default="DEBUG")
@click.option("--log_file", default="AsyncForward.log")
def run(local, remote, level, log_file):
    set_logger(level, log_file)
    async_server = AsyncServer(tuple(local.split(":")), tuple(remote.split(":")))
    asyncio.run(async_server.start())


run()
