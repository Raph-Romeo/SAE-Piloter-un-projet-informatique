from socket import socket
import json

socket = socket()
socket.connect(("127.0.0.1", 5240))

message = {"url": "/test"}
data = json.dumps(message)

socket.send(data.encode())
print(data)

print(json.loads(socket.recv(1024).decode()))

message = {"url": "/url_that_does_not_exist"}
data = json.dumps(message)

socket.send(data.encode())
print(data)

print(json.loads(socket.recv(1024).decode()))

'''RESULT:

{"url": "/test"}

{'message': 'Response from url /test'}

{"url": "/url_that_does_not_exist"}

{'status': 404, 'message': 'Url not found'}

'''


socket.close()

