import socket

HOST = ("127.0.0.1", 7779)  # IP адрес и порт сервера

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(HOST)
sock.listen()

print("---------------connection start--------------")

while True:
    print("---------------waiting...--------------")
    conn, addr = sock.accept()
    print(f"С подключением: {addr}.")

    while True:
        data = conn.recv(1024).decode()
        print(f"Сервер получил '{data}'.")

        if not data:
            break
        if "exit" in data.lower():
            print("Сервер получил команду на завершение подключения.")
            conn.send("Получена команда завершения подключения.".encode())
            break
        elif data.isdigit():
            conn.send(f"Все символы в '{data}' являются цифрами.".encode())
        elif data.isalpha():
            conn.send(f"Все символы в '{data}' являются буквами.".encode())
        else:
            conn.send(f"Получена строка - '{data}'.".encode())

    break
print("---------------connection closed--------------")