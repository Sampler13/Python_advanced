import socket
import re
from datetime import datetime


HOST = ("127.0.0.1", 7776)  # IP адрес и порт сервера
OK = b'HTTP/1.1 200 OK\n'
HEADERS = b"Host: some.ru\nHost1: some1.ru\nContent-Type: text/html; charset=utf-8\n\n"
ERR_404 = b'HTTP/1.1 404 Not Found\n\n'

now = datetime.now()
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

user_data ={
    "test": 12345,

}
int_pattern = r'^/test/(\d+)/?$'
login_pattern = r'^/message/([^/]+)/([^/]+)/?$'


def check_pattern(text, pattern):
    match = re.match(pattern, text)
    if match:
        print(f'найдено совпадение {text}')
        return True
    print(f'не найдено совпадение {text}')
    return False


def check_login(login):
    user_list = list(user_data.keys())
    if login in user_list:
        return True
    return False


def return_match(text, pattern):
    return re.match(pattern, text)


def send_file(name, conn):
    try:
        with open(name.lstrip('/'), 'rb') as file:
            print(f'sendig file {name}')
            conn.send(OK)
            conn.send(HEADERS)
            conn.send(file.read())
    except IOError:
        print('file not found')
        conn.send(ERR_404)

        conn.send("file not found\n".encode())


def is_http(req):
    meth, pat, ver = req.split('\n')[0].split(" ", 2)
    if ver and 'HTTP' in ver:
        print('это http')
        return True
    print('это не http')
    return False


def is_file(path):
    formats = ['.jpg', '.png', '.gif', '.ico', '.txt', '.html', '.json']
    return any(f in path for f in formats)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(HOST)
    sock.listen()
    print("Сервер запущен и ожидает подключения...")

    while True:
        conn, addr = sock.accept()
        with conn:
            print(f"\nПодключено к {addr}")

            request = conn.recv(1024).decode()


            if request:
                print(f"Получен запрос:\n{request}")
                try:
                    if is_http(request):
                        method, path, version = request.split('\n')[0].split(" ", 2)
                        if path == '/':
                            send_file('index.html', conn)
                        elif check_pattern(path, int_pattern):
                            match = return_match(path, int_pattern)
                            print(f"Тест с номером {match.group(1)} запущен\n\n")
                            conn.send(OK)
                            conn.send(HEADERS)
                            conn.send(f"Тест с номером {match.group(1)} запущен".encode())
                        elif check_pattern(path, login_pattern):
                            match = return_match(path, login_pattern)
                            login = match.group(1)
                            message = match.group(2)
                            if check_login(login):

                                conn.send(OK)
                                conn.send(HEADERS)
                                conn.send(f"{formatted_date}"
                                          f" - сообщение от пользователя {login}"
                                          f" - {message}\n".encode())
                            else:
                                print("пользователь не найден")
                                conn.send(OK)
                                conn.send(HEADERS)
                                conn.send(f"Пользователь {login} не найден, пожалуйста, зарегистрируйтесь\n".encode())
                        elif is_file(path):
                            print(f'посылаем файл {path}')
                            send_file(path, conn)
                        else:
                            print("пришли неизвестные  данные по HTTP")
                            conn.send(OK)
                            conn.send(HEADERS)
                            conn.send(f"пришли неизвестные  данные по HTTP - {path}\n".encode())
                    else:
                        request_prep = request.split(";")
                        if len(request_prep) == 3:
                            print("получен валидный запрос")
                            login = request_prep[1].split(":")[1].strip()
                            password = request_prep[2].split(":")[1]
                            if 'reg' in request_prep[0]:
                                print("регистрация")
                                if login in user_data:
                                    print('пользователь уже существует')
                                    conn.send(f"{formatted_date} - "
                                                f'пользователь {login} '
                                                f'уже зарегистрирован. Выберите другой логин'.encode())
                                elif len(login)>= 6 and  login.isalnum() :
                                    print(f"логин {login} подходит")
                                    if len(password) >= 8 and any(c.isdigit() for c in password):
                                        print('пароль подходит, регистрируем')
                                        conn.sendall(f"{formatted_date} - "
                                                     f"пользователь {login} зарегистрирован".encode())
                                        user_data[str(login)] = str(password)
                                    else:

                                        print("пароль не подходит")
                                        conn.sendall(f"{formatted_date} - "
                                            f"Пароль должен быть минимум 8 символов и содержать 1 цифру".encode()
                                        )
                                else:
                                    print(f"логин не подходит {login}")
                                    conn.sendall(f"{formatted_date} - "
                                        f"Имя пользователя должно содержать"
                                        f"только латинские символы и цифры, минимум 6 символов".encode())
                            elif 'signin' in request_prep[0]:
                                login = request_prep[1].split(":")[1].strip()
                                password = request_prep[2].split(":")[1]
                                if login in user_data:
                                    if password == user_data[login]:
                                        print(f"{login} успешно произведен вход")
                                        conn.sendall(f"{formatted_date} - "
                                                     f"пользователь {login} произведен вход".encode()
                                                     )
                                    else:
                                        print(f"не верный пароль")
                                        conn.sendall(f"{formatted_date} - "
                                                     f"ошибка входа {login} - неверный пароль".encode()
                                                     )
                                else:
                                    print("пользователь не найден")
                                    conn.sendall(f"{formatted_date} - "
                                                 f"ошибка входа {login} - пользователь не найден".encode()
                                                )
                            else:
                                print("получен неизвестный запрос")
                                conn.sendall(f"пришли неизвестные  данные - {request}".encode())
                        else:
                            print("получен неизвестный запрос")
                            conn.sendall(f"пришли неизвестные  данные - {request}".encode())
                except Exception as e:
                    conn.close()
                    print(e)
                finally:
                    conn.close()

