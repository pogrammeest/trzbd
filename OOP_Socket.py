import socket
import asyncio
import struct
import json
import time

from Exceptions import SocketException
import settings


class Socket():
    def __init__(self):
        self.address, self.port = settings.SERVER_ADDRESS
        self.dataPackageSize = 4096
        self.encoding = settings.ENCODING

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_loop = asyncio.new_event_loop()
        self.is_working = False

    async def send_data(self, **kwargs):
        try:
            where = kwargs['where']
            del kwargs['where']
            data = self._encode_data(kwargs)
            meta_data = struct.pack(">I", len(data))
            await self.main_loop.sock_sendall(where, meta_data + data)

        except (SocketException, KeyError, UnicodeEncodeError, ConnectionError, ValueError) as exc:
            raise SocketException(exc)

    async def _recv_message(self, listened_socket: socket.socket, massage_len: int):
        massage = bytearray()

        while len(massage) < massage_len:
            packet = await self.main_loop.sock_recv(listened_socket, massage_len - len(massage))
            if packet is None:
                return None

            massage.extend(packet)
        return massage

    def _encode_data(self, data):
        return json.dumps(data).encode(self.encoding)

    def _decode_data(self, data: bytes):
        return json.loads(data.decode(self.encoding))

    async def listen_socket(self, listened_socket):
        try:
            meta_data = await self._recv_message(listened_socket, 4)
            meta_data = struct.unpack(">I", meta_data)[0]
            data = await self._recv_message(listened_socket, meta_data)
            return self._decode_data(data)
        except(SocketException, UnicodeDecodeError, json.JSONDecodeError, IndexError, ConnectionError) as exc:
            raise SocketException(exc)

    async def main(self):
        raise NotImplemented()

    def start(self):
        self.is_working = True
        self.main_loop.run_until_complete(self.main())

    def set_up(self):
        raise NotImplemented()
