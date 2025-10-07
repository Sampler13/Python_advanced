from flask import Blueprint, render_template, redirect, url_for, request, session
from database.CRUD import *
from database.model import *
from .utils import *

bp = Blueprint('routes', __name__)

@bp.route("/")
def index():
    return render_template("base.html")


@bp.route('/quizzes/')
def quizzes_view():
    quizzes = list_instances(Quiz)  # Получаем список всех
    print(quizzes)
    return render_template('quizzes.html', quizzes=quizzes)


@bp.route("/quiz_modal/<int:quiz_id>")
def open_quiz(quiz_id):
    quiz = get_instance(Quiz, quiz_id)
    questions = quiz.questions
    shuffle_quizzes(questions)
    print(quiz)
    return render_template('quiz_start_modal.html', quiz=quiz)