from OOP_Socket import Socket
import asyncio
from datetime import datetime
from os import system
from Encryption import Encryptor
from Exceptions import SocketException
from sys import platform
import json


class Client(Socket):
    def __init__(self):

        self.messages = ""
        self.encryptor = Encryptor()

        super(Client, self).__init__()

    def set_up(self):
        try:
            self.socket.connect((self.address, self.port))

        except ConnectionError:
            print("Sorry, server is offline")
            exit(0)
        self.socket.setblocking(False)

    async def listen_socket(self, listened_socket):
        while True:
            if not self.is_working:
                return
            try:
                data = await super(Client, self).listen_socket(listened_socket)
            except SocketException as exc:
                print(exc)
                self.is_working = False
                break
            decrypted_data = json.loads(self.encryptor.decrypt(data['data']))
            self.messages += f"{decrypted_data['message_time']}: {decrypted_data['message_text']}\n"

            if platform == 'win32':
                system("cls")
            else:
                system("clear")
            print(self.messages)

    async def send_data(self, data=None):
        while True:
            message = await self.main_loop.run_in_executor(None, input, ":::")
            if not self.is_working:
                return

            encrypted_data = self.encryptor.encrypt(json.dumps(
                {
                    'message_text': message,
                    'message_time': f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"

                }
            ))

            await super(Client, self).send_data(where=self.socket, data=encrypted_data)

    async def main(self):
        await asyncio.gather(
            self.main_loop.create_task(self.listen_socket(self.socket)),
            self.main_loop.create_task(self.send_data())
        )


if __name__ == '__main__':
    client = Client()
    client.set_up()
    client.start()
