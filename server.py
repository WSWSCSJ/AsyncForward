from asyncio.streams import start_server, open_connection
from loguru import logger

from pipeline import DuplexPipeline


class AsyncServer:
    """
    基于asyncio的异步服务器
    """

    def __init__(self, local_address, remote_address, **kwargs):
        self.local_host = local_address[0]
        self.local_port = local_address[1]
        self.remote_host = remote_address[0]
        self.remote_port = remote_address[1]

    async def forward(self, reader, writer):
        local_connection = (reader, writer)
        remote_connection = await open_connection(self.remote_host, self.remote_port)
        pipeline = DuplexPipeline(local_connection, remote_connection)
        await pipeline.establish()

    async def start(self):
        """
        start async server
        """
        logger.info("AsyncServer" +
                    f" listen on {self.local_host}:{self.local_port}" +
                    f" forward to {self.remote_host}:{self.remote_port}")

        server = await start_server(self.forward, self.local_host, self.local_port)

        async with server:
            await server.serve_forever()
