from socket import socket
import time
import json

socket = socket()
socket.connect(("127.0.0.1", 5240))

message = {"url": "/auth", "method": "POST", "data": {"username": "toto", "password": "toto"}}
data = json.dumps(message)

socket.send(data.encode())
print(json.loads(socket.recv(1024).decode()))



socket.close()

