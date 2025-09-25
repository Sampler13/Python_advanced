import json
import re
import os
from config import Config

USERS_FILE = Config.USERS_FILE

# Регулярные выражения
name_re = re.compile(r'^[А-Яа-яЁё-]{2,50}$')
login_re = re.compile(r'^[A-Za-z0-9_]{6,20}$')
password_re = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)\S{8,15}$')
email_re = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')


def load_users():

    if not os.path.exists(USERS_FILE):
        print("Файл users.json не найден.")
        return {"logins": {}, "emails": {}}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("Загруженные данные пользователей:", data)
            return data
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON в файле.")
        return {"logins": {}, "emails": {}}
    except Exception as e:
        print("Произошла ошибка:", e)
        return {"logins": {}, "emails": {}}

def has_any_errors(errors_dict):
    return any(len(v) > 0 for v in errors_dict.values())

def save_users(data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:

        json.dump(data, f, ensure_ascii=False, indent=2)


def validate_registration(form):
    errors = {
        "name": validate_name(form.get('name', '').strip()),
        "surname": validate_surname(form.get('surname', '').strip()),
        "age": validate_age(form.get('age', '').strip()),
        "email": validate_email(form.get('email', '').strip()),
        "login": validate_login(form.get('login', '').strip()),
        "password": validate_password(form.get('password', '')),
    }

    return errors


def validate_name(name: str) -> list[str]:
    errors = []
    if not name_re.match(name):
        errors.append("Имя: только русские буквы (возможен дефис), длина 2–50.")
    return errors


def validate_surname(surname: str) -> list[str]:
    errors = []
    if not name_re.match(surname):
        errors.append("Фамилия: только русские буквы (возможен дефис), длина 2–50.")
    return errors


def validate_age(age_str: str) -> list[str]:
    errors = []
    try:
        age = int(age_str)
        if age < 12 or age > 100:
            errors.append("Возраст должен быть целым числом от 12 до 100.")
    except ValueError:
        errors.append("Возраст должен быть целым числом от 12 до 100.")
    return errors


def validate_email(email: str) -> list[str]:
    errors = []
    if not email_re.match(email):
        errors.append("Email должен быть валидным.")
    return errors


def validate_login(login: str) -> list[str]:
    errors = []
    if not login_re.match(login):
        errors.append("Логин: латиница, цифры и _, длина 6–20.")
    return errors


def validate_password(password: str) -> list[str]:
    errors = []
    if not password_re.match(password):
        errors.append("Пароль: 8–15 символов, минимум 1 строчная лат., 1 заглавная лат. и 1 цифра, без пробелов.")
    return errors