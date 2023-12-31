import socket, views, threading, sys, json, time, datetime
from cryptography.fernet import Fernet
from settings import *
import mysql.connector


class Request:
    """
    Object Request is used to format the client's request to be managed more easily.
    """
    def __init__(self, request, client):
        self.client = client
        if "t" in request.keys():
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
    """
    Object User is used to handle the connection after a request was passed to the server.
    """
    def __init__(self, is_authenticated: bool, data: dict = None):
        self.is_authenticated = is_authenticated
        self.data = data


class View:
    """
    Object View is used to manage the different URL paths, and which view function it points to from views.py.
    """
    def __init__(self, view, protected: bool = False):
        self.view = view
        self.protected = protected


class Client:
    """
    Object Client is used to handle a socket connection to the server.
    """
    def __init__(self, serv: object, connection: object, addr: str, secret_key):
        print(f"NEW CONNECTION : {addr[0]}:{addr[1]}")
        self.server = serv
        self.connection = connection
        self.addr = addr
        self.secret_key = secret_key
        self.connected = True
        self.client_thread = threading.Thread(target=self.handle)
        self.client_thread.start()

    def close(self) -> None:
        """
        Properly close connection when socket is closed or when connection is lost.
        """
        #print(f"CONNECTION CLOSED : {self.addr[0]}:{self.addr[1]}")
        self.connection.close()
        self.connected = False
        try:
            self.database_connection.close()
        except:
            pass
        return

    def handle(self) -> None:
        """
        Thread function used to listen to the client's requests in a loop without blocking main thread.
        """
        while self.connected:
            try:
                data = self.connection.recv(1024)
                if len(data) > 0:
                    data = Request(json.loads(data.decode("utf-8")), self)
                    if data.test:
                        self.connection.send(json.dumps({"status": 200}).encode())
                    else:
                        self.database_connection = mysql.connector.connect(
                            host=database_params["host"],
                            port=database_params["port"],
                            user=database_params["user"],
                            password=database_params["password"],
                            database=database_params["database"]
                        )
                        while self.database_connection is None:
                            time.sleep(0.1)
                        self.connection.send(self.server.request(data))
                else:
                    self.close()
            except:
                self.close()
        return

    def verify_token(self, request):
        """
        SECURITY | Method used to verify if the client request's token is valid
        """
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
        """
        When authentication was made with the client, using the username and password, a token is generated.
        The current datetime is added, and the whole string is salted using the server's secret key.
        """
        fernet = Fernet(self.secret_key)
        token = f"{username},{password},{datetime.datetime.now()}"
        token = fernet.encrypt(token.encode())
        return token

    def check_username(self, username):
        """
        Check if username STRING argument already exists in the mysql database in the User table.
        """
        cursor = self.database_connection.cursor()
        query = "SELECT * FROM User WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def check_email(self, email):
        """
        Check if Email STRING argument already exists in the mysql database in the User table.
        """
        cursor = self.database_connection.cursor()
        query = "SELECT * FROM User WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def check_username_and_password(self, username, password):
        """
        Check if username STRING argument and password (MD5) STRING argument are valid in the mysql database in the
        User table.
        """
        cursor = self.database_connection.cursor()
        query = "SELECT * FROM User WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        return result


class Server:
    """
    Main class for the server.
    Server class initiates the server using python sockets module.
    """
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
            # Users + AUTHENTICATION
            "/auth": View(views.login, protected=False),
            "/create_user": View(views.create_user, protected=False),
            # Tasks CRUD
            "/tasks": View(views.tasks, protected=True),
            "/set_completed": View(views.set_completed, protected=True),
            "/delete_task": View(views.delete_task, protected=True),
            "/delete_tasks": View(views.delete_tasks, protected=True),
            "/create_task": View(views.create_task, protected=True),
            "/task_details": View(views.task_details, protected=True),
            # "/update_task": View(views.update_task, protected=True),
            # Friends system
            "/fetch_requests": View(views.fetch_requests, protected=True),
            "/friend_request": View(views.friend_request, protected=True),
            "/friends": View(views.friends, protected=True),
            "/deny_friend_request": View(views.deny_friend_request, protected=True),
            "/cancel_friend_request": View(views.cancel_friend_request, protected=True),
            "/accept_friend_request": View(views.accept_friend_request, protected=True),
            "/unfriend": View(views.remove_friend, protected=True),
        }

    def close(self) -> None:
        """
        Properly shuts down the server and all threads.
        """
        self.forceStop = True
        self.socket.close()
        return

    def start(self) -> bool:
        """
        Start the server socket.
        """
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
        """
        Listening for client connections ( THREAD LOOP )
        """
        self.socket.listen()
        while not self.forceStop:
            conn, addr = self.socket.accept()
            self.clients.append(Client(self, conn, addr, self.secret_key))

    def remove(self, client):
        """
        Remove a client from the list of clients (self.clients:list)
        """
        self.clients.remove(client)

    def request(self, request: object) -> bytes:
        """
        Handle a request from the client.
        Verify URL existence -> Execute Views function associated to request's URL.
        """
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
        except Exception as err:
            print(err)
            return json.dumps({"status": 400, "message": "Invalid request"}).encode()


if __name__ == "__main__":
    """
    CREATE SERVER AND START SERVER
    """
    server = Server()
    sys.exit(server.start())

