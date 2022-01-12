import asyncio

from server import AsyncServer
from logger import set_logger

set_logger("DEBUG")

async_server = AsyncServer(('127.0.0.1', 9000), ('127.0.0.1', '6379'))

try:
    asyncio.get_event_loop().run_until_complete(async_server.start())
except RuntimeError:
    asyncio.run(async_server.start())
