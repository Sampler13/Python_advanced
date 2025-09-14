import socket

HOST = ("127.0.0.1", 7776)

# Создаем соединение


def send_message(com, log, pas):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(HOST)
    sock.send(f"command:{com}; login:{log}; password:{pas}".encode())
    print(sock.recv(1024).decode())
    sock.close()

send_message('reg', 'igor', '123')
send_message('reg', 'igorigor', '123')
send_message('reg', 'igorigor!@', '123qwerT')
send_message('reg', 'igorigor', '123qwerT')
send_message('reg', 'igorigor123', '123qwerT')
send_message('reg', 'test', '123')


send_message('signin', 'igorigor', '123qwer')
send_message('signin', 'igorigor', '123qwerT')
send_message('signin', 'vasya', '123qwerT')
send_message('blabla', 'igorigor', '123qwerT')


# это для теста =)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(HOST)

sock.send(f"command:singin; login:igor; password:123; asdasdsadasd".encode())
print(sock.recv(1024).decode())