from socket import socket
import time

socket = socket()
socket.connect(("127.0.0.1", 5240))
socket.send("test".encode())
time.sleep(5)
socket.close()

