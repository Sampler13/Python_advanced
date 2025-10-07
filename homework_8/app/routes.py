# routes.py — упрощённые маршруты без "админ" и без таблиц

from flask import Blueprint, render_template, redirect, url_for, request, session
from database.CRUD import *  # оставляю твои CRUD-хелперы; используем list_instances
from database.model import db, User, Quiz, Question
from .utils import get_quiz, build_options, state_key

bp = Blueprint('routes', __name__)

@bp.route("/")
def index():
    return render_template("base.html")


@bp.route('/quizzes/')
def quizzes_view():
    quizzes = list_instances(Quiz)
    return render_template('quizzes.html', quizzes=quizzes)


@bp.route("/quiz/<int:quiz_id>/go", methods=["GET", "POST"])
def quiz_go(quiz_id):
    quiz = get_quiz(quiz_id)
    key = state_key(quiz_id)


    if request.method == "GET" and request.args.get("new"):
        session.pop(key, None)

    state = session.get(key)
    if not state:
        questions = list(getattr(quiz, "questions", []))
        order = [q.id for q in questions]
        state = {"i": 0, "score": 0, "order": order, "opts": {}}
        session[key] = state

    order = state["order"]
    i = state["i"]
    total = len(order)

    if total == 0:
        session.pop(key, None)
        return render_template("quiz_run.html", quiz=quiz, finished=True, score=0, total=0)

    if request.method == "POST":
        if i < total:
            qid = order[i]
            question = next((q for q in quiz.questions if q.id == qid), None)


            opts_map = state.get("opts", {})
            options = opts_map.get(str(qid))
            if not options:
                options, _ = build_options(question)


            try:
                sel_idx = int(request.form.get("answer_idx"))
            except (TypeError, ValueError):
                sel_idx = -1

            selected_text = None
            if options and 0 <= sel_idx < len(options):
                selected_text = options[sel_idx]


            _, correct_text = build_options(question)
            if correct_text and selected_text == correct_text:
                state["score"] += 1

            state["i"] += 1
            session[key] = state

        return redirect(url_for("routes.quiz_go", quiz_id=quiz_id))

    if i >= total:
        score = state["score"]
        session.pop(key, None)
        return render_template("quiz_run.html", quiz=quiz, finished=True, score=score, total=total)


    qid = order[i]
    question = next((q for q in quiz.questions if q.id == qid), None)

    opts_map = state.get("opts", {})
    options = opts_map.get(str(qid))
    if not options:
        options, _ = build_options(question)
        state.setdefault("opts", {})[str(qid)] = options
        session[key] = state

    current = i + 1
    return render_template(
        "quiz_run.html",
        quiz=quiz,
        finished=False,
        question=question,
        options=options,
        current=current,
        total=total
    )


@bp.route("/quizzes/manage", methods=["GET"])
def quizzes_manage():
    # Основной список
    quizzes = list_instances(Quiz)
    questions = list_instances(Question)


    sel_id = request.args.get("quiz_id", type=int)
    selected_quiz = None
    available_questions = []
    if sel_id:
        selected_quiz = Quiz.query.get(sel_id)
        if selected_quiz:
            attached_ids = {q.id for q in selected_quiz.questions}
            available_questions = [q for q in questions if q.id not in attached_ids]

    return render_template(
        "quizzes_manage.html",
        quizzes=quizzes,
        questions=questions,
        selected_quiz=selected_quiz,
        available_questions=available_questions
    )


@bp.route("/quizzes/create", methods=["POST"])
def quiz_create():
    name = (request.form.get("name") or "").strip()
    user_id = request.form.get("user_id", type=int)
    if not name:
        return redirect(url_for("routes.quizzes_manage"))

    if not user_id:

        user = User.query.first()
        if not user:
            user = User(name="Demo")
            db.session.add(user)
            db.session.commit()
        user_id = user.id
    qz = Quiz(name=name, user_id=user_id)
    db.session.add(qz)
    db.session.commit()
    return redirect(url_for("routes.quizzes_manage", quiz_id=qz.id))

@bp.route("/quizzes/<int:quiz_id>/rename", methods=["POST"])
def quiz_rename(quiz_id):
    qz = Quiz.query.get_or_404(quiz_id)
    name = (request.form.get("name") or "").strip()
    if name:
        qz.name = name
        db.session.commit()
    return redirect(url_for("routes.quizzes_manage", quiz_id=qz.id))

@bp.route("/quizzes/<int:quiz_id>/delete", methods=["POST"])
def quiz_delete(quiz_id):
    qz = Quiz.query.get_or_404(quiz_id)

    qz.questions.clear()
    db.session.delete(qz)
    db.session.commit()
    return redirect(url_for("routes.quizzes_manage"))


@bp.route("/quizzes/<int:quiz_id>/attach", methods=["POST"])
def quiz_attach(quiz_id):
    qz = Quiz.query.get_or_404(quiz_id)
    question_id = request.form.get("question_id", type=int)
    if question_id:
        q = Question.query.get_or_404(question_id)
        if q not in qz.questions:
            qz.questions.append(q)
            db.session.commit()
    return redirect(url_for("routes.quizzes_manage", quiz_id=qz.id))

@bp.route("/quizzes/<int:quiz_id>/detach/<int:question_id>", methods=["POST"])
def quiz_detach(quiz_id, question_id):
    qz = Quiz.query.get_or_404(quiz_id)
    q = Question.query.get_or_404(question_id)
    if q in qz.questions:
        qz.questions.remove(q)
        db.session.commit()
    return redirect(url_for("routes.quizzes_manage", quiz_id=qz.id))

@bp.route("/quizzes/<int:quiz_id>/quick-add", methods=["POST"])
def quiz_quick_add_question(quiz_id):
    qz = Quiz.query.get_or_404(quiz_id)
    text = (request.form.get("text") or "").strip()
    answer = (request.form.get("answer") or "").strip()
    wrong1 = (request.form.get("wrong1") or "").strip()
    wrong2 = (request.form.get("wrong2") or "").strip()
    wrong3 = (request.form.get("wrong3") or "").strip()
    if text and answer and wrong1 and wrong2 and wrong3:
        q = Question(text=text, answer=answer, wrong1=wrong1, wrong2=wrong2, wrong3=wrong3)
        db.session.add(q)
        db.session.flush()
        qz.questions.append(q)
        db.session.commit()
    return redirect(url_for("routes.quizzes_manage", quiz_id=qz.id))


@bp.route("/questions/create", methods=["POST"])
def question_create():
    text = (request.form.get("text") or "").strip()
    answer = (request.form.get("answer") or "").strip()
    wrong1 = (request.form.get("wrong1") or "").strip()
    wrong2 = (request.form.get("wrong2") or "").strip()
    wrong3 = (request.form.get("wrong3") or "").strip()
    if text and answer and wrong1 and wrong2 and wrong3:
        q = Question(text=text, answer=answer, wrong1=wrong1, wrong2=wrong2, wrong3=wrong3)
        db.session.add(q)
        db.session.commit()
    return redirect(url_for("routes.quizzes_manage"))

@bp.route("/questions/<int:question_id>/edit", methods=["GET", "POST"])
def question_edit(question_id):
    q = Question.query.get_or_404(question_id)
    if request.method == "POST":
        text = (request.form.get("text") or "").strip()
        answer = (request.form.get("answer") or "").strip()
        wrong1 = (request.form.get("wrong1") or "").strip()
        wrong2 = (request.form.get("wrong2") or "").strip()
        wrong3 = (request.form.get("wrong3") or "").strip()
        if text and answer and wrong1 and wrong2 and wrong3:
            q.text = text
            q.answer = answer
            q.wrong1 = wrong1
            q.wrong2 = wrong2
            q.wrong3 = wrong3
            db.session.commit()

            return redirect(url_for("routes.quizzes_manage"))
        return render_template("question_form.html", question=q, error="Заполните все поля")
    return render_template("question_form.html", question=q)

@bp.route("/questions/<int:question_id>/delete", methods=["POST"])
def question_delete(question_id):
    q = Question.query.get_or_404(question_id)

    for quiz in list(q.quizzes):
        quiz.questions.remove(q)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("routes.quizzes_manage"))


@bp.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'