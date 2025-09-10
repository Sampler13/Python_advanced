import socket
import time

HOST = ("127.0.0.1", 7779)  # IP адрес и порт сервера

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(HOST)

sock.send("Привет".encode())
print(sock.recv(1024).decode())
time.sleep(5)
sock.send("12345".encode())
print(sock.recv(1024).decode())
time.sleep(5)
sock.send("i want to exit".encode())
print(sock.recv(1024).decode())

sock.close()