from flask import Blueprint, render_template, redirect, url_for, request, session
from .forms import validate_registration, load_users, save_users, validate_login, has_any_errors, validate_password
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import get_request, weather_request, login_required

bp = Blueprint('routes', __name__)


@bp.route("/")
def index():
    user_login = session.get('user_login')
    user_name = session.get('user_name')
    user_surname = session.get('user_surname')
    return render_template('index.html',
                           user_login=user_login,
                           user_name=user_name,
                           user_surname=user_surname)


@bp.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html', form={}, errors={})

    form = request.form.to_dict()

    errors = {
        "login": validate_login(form['login']),
        "password": validate_password(form['password']),
    }

    if not has_any_errors(errors):
        users = load_users()
        login_value = form['login']
        password = form['password']

        user = users['logins'].get(login_value)
        name = user['name'] if user else None
        surname = user['surname'] if user else None
        if user and check_password_hash(user['password_hash'], password):
            session['user_login'] = login_value
            session['user_name'] = name
            session['user_surname'] = surname
            return redirect(url_for('routes.index'))
        else:
            errors['login'].append("Неверный логин или пароль.")  #

    return render_template('login.html', form=form, errors=errors)


@bp.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('registration.html', form={}, errors={})

    form = request.form.to_dict()
    errors = validate_registration(form)

    if not has_any_errors(errors):
        users = load_users()

        login_value = form['login']
        email_value = form['email']
        if login_value in users['logins']:
            errors.setdefault('login', []).append('Такой логин уже существует.')

        if email_value in users['emails']:
            errors.setdefault('email', []).append('Пользователь с таким email уже зарегистрирован.')

        if has_any_errors(errors):

            return render_template('registration.html', form=form, errors=errors)
        password_hash = generate_password_hash(form['password'])
        user_record = {
            "name": form['name'],
            "surname": form['surname'],
            "age": int(form['age']),
            "email": email_value,
            "password_hash": password_hash
        }
        users['logins'][login_value] = user_record
        users['emails'][email_value] = login_value
        save_users(users)

        return redirect(url_for('routes.login'))

    return render_template('registration.html', form=form, errors=errors)

@bp.route("/duck/", endpoint='get_duck')
@login_required
def get_duck():
    user_login = session.get('user_login')
    user_name = session.get('user_name')
    user_surname = session.get('user_surname')
    image = get_request('https://random-d.uk/api/random')
    img_trim = image.rstrip('.jpg').rstrip('.gif').split('/')[-1]
    return render_template('duck.html',
                           link=image,
                           num=img_trim,
                           user_login=user_login,
                           user_name=user_name,
                           user_surname=user_surname
                           )

@bp.route("/fox/<int:count>/", endpoint='get_fox')
@login_required
def get_fox(count):
    user_login = session.get('user_login')
    user_name = session.get('user_name')
    user_surname = session.get('user_surname')
    fox_list = []
    if count > 10 or count < 1:
        return render_template('fox.html', err=True)
    else:
        for i in range(count):
            fox_list.append(get_request('https://randomfox.ca/floof'))
        return render_template('fox.html',
                               foxes=fox_list,
                               user_login=user_login,
                               user_name=user_name,
                               user_surname=user_surname
                               )


@bp.route("/weather/<city>/", endpoint='get_weather')
@login_required
def get_weather(city):
    user_login = session.get('user_login')
    user_name = session.get('user_name')
    user_surname = session.get('user_surname')
    weather_data = weather_request(city)
    if weather_data:
        return render_template('weather.html',
                               weather=weather_data,
                               err=False,
                               user_login=user_login,
                               user_name=user_name,
                               user_surname=user_surname
                               )
    else:
        return render_template('weather.html',
                               weather=None,
                               err=True,
                               user_login=user_login,
                               user_name=user_name,
                               user_surname=user_surname
                               )

@bp.route("/weather-minsk/", endpoint='get_weather_minsk')
@login_required
def get_weather_minsk():
    user_login = session.get('user_login')
    user_name = session.get('user_name')
    user_surname = session.get('user_surname')
    return redirect(url_for('routes.get_weather',
                            city='minsk',
                            user_login=user_login,
                            user_name=user_name,
                            user_surname=user_surname
                            ))


@bp.route("/logout/", endpoint='logout')
@login_required
def logout():
    session.pop('user_login', None)
    return redirect(url_for('routes.index'))


@bp.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'