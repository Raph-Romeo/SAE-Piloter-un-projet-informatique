import socket, threading, sys, time

server_port = 5240

class Server:
    def __init__(self):

        # server parameters
        self.port = server_port
        self.max_number_of_attempts = 5  # When server start fails, it will re-attempt X times.

        # server attributes:
        self.forceStop = False
        self.socket = socket.socket()
        self.clients = []
        self.number_of_attempts = 0

    def close(self) -> None:
        self.forceStop = True
        self.socket.close()
        return

    def start(self) -> bool:
        try:
            self.number_of_attempts += 1
            self.socket.bind(("0.0.0.0", self.port))
        except socket.error as msg:
            if self.number_of_attempts < self.max_number_of_attempts:
                print(f"Attempt {self.number_of_attempts}/{self.max_number_of_attempts} - Socket binding error: {str(msg)}\nRetrying in 5 seconds...")
                time.sleep(5)
                return self.start()
        else:
            listen_thread = threading.Thread(target=self.listen)
            listen_thread.start()
            print(f"SERVER SUCCESSFULLY STARTED ON PORT : {self.port}")
            print("WAITING FOR CLIENTS...")
            return True

    def listen(self):
        self.socket.listen()
        while not self.forceStop:
            self.clients.append(self.socket.accept())


if __name__ == "__main__":
    server = Server()
    sys.exit(server.start())
