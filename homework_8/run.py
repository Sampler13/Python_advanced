from app import create_app
from database.service import *
app = create_app()

questions_data = [
    Question('Сколько будут 2+2*2', '6', '8', '2', '0'),
    Question('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
    Question('Каким станет зелёный утёс, если упадет в Красное море?', 'Мокрым?', 'Красным', 'Не изменится', 'Фиолетовым'),
    Question('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
    Question('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
    Question('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
    Question('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако'),
    Question('Что такое у меня в кармашке?', 'Кольцо', 'Кулак', 'Дырка', 'Бублик')
]

# with app.app_context():
    # create_users(3)
    # create_quizzes(4)
    # parse_and_create_questions(questions_data)
    # add_random_questions(1, 3)
    # add_random_questions(2, 4)
    # add_random_questions(3, 2)
    # add_random_questions(4, 6)
    # reset_db()
    # quiz = get_instance(Quiz, 4)
    # questions = quiz.questions

if __name__ == "__main__":
    app.run(debug=False, port=5001)

