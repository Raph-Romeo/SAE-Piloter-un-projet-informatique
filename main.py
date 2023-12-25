import socket, sys, time

class Server:
    def __init__(self):
        self.socket = socket.socket()

    def close(self) -> None:
        self.socket.close()
        return

    def start(self) -> bool:
        try:
            self.socket.bind(("0.0.0.0", 5240))
        except socket.error as msg:
            if self.number_of_attempts < self.max_number_of_attempts:
                print(msg)
                print("trying again in 5 seconds...")
                time.sleep(5)
                return self.start()
        else:
            print(f"SERVER SUCCESSFULLY STARTED ON PORT : 5240")
            return True


if __name__ == "__main__":
    server = Server()
    sys.exit(server.start())

