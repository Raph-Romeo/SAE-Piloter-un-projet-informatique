import socket, views, threading, sys, json, time, datetime
from settings import *
import mysql.connector


class Request:
    def __init__(self, request, client):
        self.client = client
        if "url" in request.keys():
            self.url = request["url"]
        else:
            self.url = None
        print(self.url, self.client.addr)


class View:
    def __init__(self, view):
        self.view = view


class Client:
    def __init__(self, serv: object, connection: object, addr: str):
        print(f"NEW CONNECTION : {addr[0]}:{addr[1]}")
        self.server = serv
        self.connection = connection
        self.addr = addr
        self.connected = True
        self.client_thread = threading.Thread(target=self.handle)
        self.client_thread.start()
        self.database_connection = None
        # self.database_connection = mysql.connector.connect(
        #    host=database_params["host"],
        #    port=database_params["port"],
        #    user=database_params["user"],
        #    password=database_params["password"],
        #    database=database_params["database"]
        #)

    def close(self) -> None:
        print(f"CONNECTION CLOSED : {self.addr[0]}:{self.addr[1]}")
        self.server.remove(self)
        self.connection.close()
        self.connected = False
        # self.database_connection.close()
        return

    def handle(self) -> None:
        while self.connected:
            try:
                data = self.connection.recv(1024)
                if len(data) > 0:
                    data = Request(json.loads(data.decode("utf-8")), self)
                    self.connection.send(self.server.request(data))
                else:
                    self.close()
            except Exception as err:
                print(err)
                self.close()
        return


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

        # server URLS:
        self.urls = {
            "/test": View(views.test),
        }

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
            conn, addr = self.socket.accept()
            self.clients.append(Client(self, conn, addr))

    def remove(self, client):
        self.clients.remove(client)

    def request(self, request: object) -> bytes:
        try:
            if request.url in self.urls.keys():
                return self.urls[request.url].view(request)
            else:
                return json.dumps({"status": 404, "message": "Url not found"}).encode()
        except:
            return json.dumps({"status": 400, "message": "Invalid request"}).encode()


if __name__ == "__main__":
    server = Server()
    sys.exit(server.start())

