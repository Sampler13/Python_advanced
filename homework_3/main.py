import os
import requests
from flask import Flask, render_template, redirect, url_for

BASE_DIR = os.path.dirname(__name__)

app = Flask(__name__)


def get_request(url):
    res = requests.get(url)

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

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/duck/")
def get_duck():
    image = get_request('https://random-d.uk/api/random')
    img_trim = image.rstrip('.jpg').rstrip('.gif').split('/')[-1]
    return render_template('duck.html', link=image, num=img_trim)

@app.route("/fox/<int:count>/")
def get_fox(count):
    fox_list = []
    if count > 10 or count < 1:
        return render_template('fox.html', err=True)
    else:
        for i in range(count):
            fox_list.append(get_request('https://randomfox.ca/floof'))
        return render_template('fox.html', foxes=fox_list)


@app.route("/weather/<city>/")
def get_weather(city):
        weather_data = weather_request(city)
        if weather_data:
            return render_template('weather.html', weather=weather_data, err=False)
        else:
            return render_template('weather.html',weather=None, err=True)

@app.route("/weather-minsk/")
def get_weather_minsk():
    return redirect(url_for('get_weather', city='minsk'))

@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)