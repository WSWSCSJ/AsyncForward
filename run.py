import click
import asyncio

from server import AsyncServer
from logger import set_logger


@click.command()
@click.option("--local")
@click.option("--remote")
def run(local, remote):
    set_logger("INFO", "log.log")
    async_server = AsyncServer(tuple(local.split(":")), tuple(remote.split(":")))
    asyncio.run(async_server.start())


run()
