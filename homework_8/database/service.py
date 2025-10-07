from .model import  *
from .CRUD import *
import random



def create_users(count):
    for i in range(1, count + 1):
        print(i)
        create_instance(User, name=f"User{i}")

def create_quizzes(num):
    for i in range(1, num + 1):
        user = get_instance(User, 1)
        print(i)
        create_instance(Quiz, name=f'Quiz{i}', user_id=user.id)


def create_question(text, answer, wrong1, wrong2, wrong3):
    question_instance = create_instance(Question, text=text, answer=answer, wrong1=wrong1, wrong2=wrong2, wrong3=wrong3)
    return question_instance

def parse_and_create_questions(questions):
    for q in questions:
        create_instance(Question, text=q.text, answer=q.answer, wrong1=q.wrong1, wrong2=q.wrong2, wrong3=q.wrong3)
    return True

def add_random_questions(quiz_id, number_quest):
    quiz = get_instance(Quiz, quiz_id)

    if not quiz:
        return

    questions = list_instances(Question)

    if len(questions) < number_quest:
        return

    random_questions = random.sample(questions, number_quest)

    for question in random_questions:
        quiz.questions.append(question)

    db.session.commit()


