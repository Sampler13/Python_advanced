
import requests
from flask import session, redirect, url_for


def get_request(url):
    res = requests.get(url, verify=False)

    try:
        result = res.json()
    except ValueError:
        print("Ответ не является корректным JSON.")
        return None

    if 'image' in result:
        return result['image']
    elif 'url' in result:
        return result['url']
    else:
        return None


def weather_request(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
        res = requests.get(url, params)
        res = res.json()

        # https://openweathermap.org/weather-conditions - ссылка на документацию
        weather_info = {
            "city": res['name'],
            "country": res['sys']['country'],
            "temp": round(res['main']['temp'] - 273.15, 1),
            "description": res['weather'][0]['description'],
            "icon": f"http://openweathermap.org/img/wn/{res['weather'][0]['icon']}@2x.png"
        }

        return weather_info

    except Exception as e:
        print(e)


def login_required(f):
    def wrapped_function(*args, **kwargs):
        if 'user_login' not in session:
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return wrapped_function