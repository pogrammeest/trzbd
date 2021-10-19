from OOP_Socket import Socket
import asyncio
from Exceptions import SocketException
import json


class Server(Socket):

    def __init__(self):
        super(Server, self).__init__()

        self.users = []

    def set_up(self):
        self.socket.bind((self.address, self.port))
        self.socket.listen()
        self.socket.setblocking(False)
        print("Server listing...")

    async def send_data(self, **kwargs):
        for user in self.users:
            try:
                await super(Server, self).send_data(where=user, data=kwargs['data'])
            except SocketException as exc:
                print(exc)
                user.close()

    async def listen_socket(self, listened_socket=None):
        while True:
            try:
                # print(self.users)
                data = await super(Server, self).listen_socket(listened_socket)
                await self.send_data(data=data['data'])
            except SocketException as exc:
                print(f"User {listened_socket.getpeername()[0]}:{listened_socket.getpeername()[1]} has disconnected.")
                self.users.remove(listened_socket)
                listened_socket.close()

                return

    async def accept_socket(self):
        while True:
            client_socket, client_address = await self.main_loop.sock_accept(self.socket)  # blocking
            print(f"User {client_address[0]} connected!")
            self.users.append(client_socket)
            self.main_loop.create_task(self.listen_socket(client_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_socket())


if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.start()
