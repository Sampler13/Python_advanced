from database.model import *
from database.CRUD import *
import random

def state_key(quiz_id: int) -> str:
    return f"quiz_run_{quiz_id}"
def get_quiz(quiz_id: int):
    quiz = get_instance(Quiz, quiz_id)

    return quiz
def build_options(question):

    correct = getattr(question, "answer", None)
    w1 = getattr(question, "wrong1", None)
    w2 = getattr(question, "wrong2", None)
    w3 =  getattr(question, "wrong3", None)

    opts = []
    if isinstance(correct, str) and correct.strip():
        opts.append(correct.strip())
    for w in (w1, w2, w3):
        if isinstance(w, str) and w.strip():
            opts.append(w.strip())


    random.shuffle(opts)
    return opts, correct.strip()


