import socket, sys

class Server:
    def __init__(self):
        self.socket = socket.socket()

    def start(self) -> bool:
        self.socket.bind(("0.0.0.0", 5240))
        print(f"SERVER SUCCESSFULLY STARTED ON PORT : 5240")


if __name__ == "__main__":
    server = Server()
    sys.exit(server.start())

