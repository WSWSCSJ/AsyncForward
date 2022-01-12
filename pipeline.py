import asyncio

from loguru import logger


class DuplexPipeline:
    """
    pipeline:
        | local asyncio.stream.StreamReader --->  data ---> remote asyncio.stream.StreamWriter |
        | local asyncio.stream.StreamWriter <---  data <--- remote asyncio.stream.StreamReader |

    read Data from local StreamReader, and write Data to remote StreamWriter
    read Data from remote StreamReader, and write Data to local StreamWriter
    """

    class STATUS:
        READY = "READY"
        RUNNING = "RUNNING"
        CLOSED = "CLOSED"

    status = STATUS.READY
    chunk_size = 1024

    def __init__(self, local_connection, remote_connection, **kwargs):
        self.local_reader = local_connection[0]
        self.local_writer = local_connection[1]
        self.remote_reader = remote_connection[0]
        self.remote_writer = remote_connection[1]

        local_peer = self.local_writer.get_extra_info("peername")
        local_sock = self.local_writer.get_extra_info("sockname")
        remote_peer = self.remote_writer.get_extra_info("peername")

        self.info = {
            "local_peer": f"{local_peer[0]}:{local_peer[1]}",
            "local_sock": f"{local_sock[0]}:{local_sock[1]}",
            "remote_peer": f"{remote_peer[0]}:{remote_peer[1]}",
        }
        self.info['stream'] = f"<{self.info['local_peer']} <---> " \
                              f"{self.info['local_sock']} <---> " \
                              f"{self.info['remote_peer']}>"

        self.pipeline = (
            self.transport(self.local_reader, self.remote_writer, self.info['local_peer'], self.info['remote_peer']),
            self.transport(self.remote_reader, self.local_writer, self.info['remote_peer'], self.info['local_peer'])
        )

        for key, value in kwargs:
            if hasattr(self, key):
                setattr(self, key, value)

        logger.debug(f"create pipeline: {self.info['stream']}")

    async def transport(self, reader, writer, reader_peer, writer_peer):
        while self.status == self.STATUS.RUNNING:
            data = await reader.read(self.chunk_size)
            if not data:
                writer.close()
                self.status = self.STATUS.CLOSED
                break
            writer.write(data)
            logger.debug(f"<{reader_peer} --> {writer_peer}>\nbinary: {data}")

        writer.close()
        await writer.wait_closed()

    async def establish(self):
        logger.debug(f"pipeline: {self.info['stream']} start")

        self.status = self.STATUS.RUNNING
        await asyncio.gather(*self.pipeline)
        await self.close()

        logger.debug(f"pipeline: {self.info['stream']} close")

    async def close(self):
        for writer in (self.local_writer, self.remote_writer):
            if not writer.is_closing():
                writer.close()
                await writer.wait_closed()
