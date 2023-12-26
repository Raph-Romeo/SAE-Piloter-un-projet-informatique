import socket, views, threading, sys, json, time, datetime
from cryptography.fernet import Fernet
from settings import *
import mysql.connector


class Request:
    def __init__(self, request, client):
        self.client = client
        if "test" in request.keys():
            self.test = True
        else:
            self.test = False
            if "url" in request.keys():
                self.url = request["url"]
            else:
                self.url = None
            if "method" in request.keys():
                self.method = request["method"]
            else:
                self.method = None
            if "data" in request.keys():
                self.data = request["data"]
            else:
                self.data = None
            if "token" in request.keys():
                self.token = request["token"]
            else:
                self.token = None
            print(self.method, self.url, self.client.addr)


class User:
    def __init__(self, is_authenticated: bool, data: dict = None):
        self.is_authenticated = is_authenticated
        self.data = data


class View:
    def __init__(self, view, protected: bool = False):
        self.view = view
        self.protected = protected


class Client:
    def __init__(self, serv: object, connection: object, addr: str, secret_key):
        print(f"NEW CONNECTION : {addr[0]}:{addr[1]}")
        self.server = serv
        self.connection = connection
        self.addr = addr
        self.secret_key = secret_key
        self.connected = True
        self.client_thread = threading.Thread(target=self.handle)
        self.client_thread.start()
        self.database_connection = mysql.connector.connect(
            host=database_params["host"],
            port=database_params["port"],
            user=database_params["user"],
            password=database_params["password"],
            database=database_params["database"]
        )

    def close(self) -> None:
        print(f"CONNECTION CLOSED : {self.addr[0]}:{self.addr[1]}")
        self.server.remove(self)
        self.connection.close()
        self.connected = False
        self.database_connection.close()
        return

    def handle(self) -> None:
        while self.connected:
            try:
                data = self.connection.recv(1024)
                if len(data) > 0:
                    data = Request(json.loads(data.decode("utf-8")), self)
                    if data.test:
                        self.connection.send(json.dumps({"status": 200}).encode())
                    else:
                        self.connection.send(self.server.request(data))
                else:
                    self.close()
            except:
                self.close()
        return

    def verify_token(self, request):
        try:
            if request.token is not None:
                fernet = Fernet(self.secret_key)
                token = fernet.decrypt(request.token.encode()).decode()
                username = token.split(",")[0]
                password = token.split(",")[1]
                date = token.split(",")[2]
                if (datetime.datetime.now() - datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')).days < 30:
                    # Checking if Token is not older than 30 days.
                    return self.check_username_and_password(username, password)
        except:
            pass
        return False

    def generate_token(self, username, password) -> bytes:
        fernet = Fernet(self.secret_key)
        token = f"{username},{password},{datetime.datetime.now()}"
        token = fernet.encrypt(token.encode())
        return token

    def check_username(self, username):
        cursor = self.database_connection.cursor()
        query = "SELECT * FROM User WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def check_username_and_password(self, username, password):
        cursor = self.database_connection.cursor()
        query = "SELECT * FROM User WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        return result


class Server:
    def __init__(self):

        # server parameters
        self.port = server_port
        self.secret_key = Fernet.generate_key()  # This key is used for encrypting tokens
        self.max_number_of_attempts = 5  # When server start fails, it will re-attempt X times.

        # server attributes:
        self.forceStop = False
        self.socket = socket.socket()
        self.clients = []
        self.number_of_attempts = 0

        # server URLS:
        self.urls = {
            "/auth": View(views.login),
            "/tasks": View(views.tasks, protected=True),
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
            self.clients.append(Client(self, conn, addr, self.secret_key))

    def remove(self, client):
        self.clients.remove(client)

    def request(self, request: object) -> bytes:
        token_check = request.client.verify_token(request)
        if token_check:
            user = User(is_authenticated=True, data=token_check)
        else:
            user = User(is_authenticated=False)
        try:
            request.user = user
            if request.url in self.urls.keys():
                if self.urls[request.url].protected:
                    if user.is_authenticated:
                        return self.urls[request.url].view(request)
                    else:
                        return json.dumps({"status": 403, "message": "Forbidden"}).encode()
                else:
                    return self.urls[request.url].view(request)
            else:
                return json.dumps({"status": 404, "message": "Url not found"}).encode()
        except:
            return json.dumps({"status": 400, "message": "Invalid request"}).encode()


if __name__ == "__main__":
    server = Server()
    sys.exit(server.start())

