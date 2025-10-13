from fastapi import APIRouter, HTTPException, Depends
from models.database import UserRepository as ur
from models.database import QuizRepository as qz
from models.database import QuestionRepository as qq
from schemas.schemas import *



default_router = APIRouter()


users_router = APIRouter(
    prefix="/users",
    tags = ["Пользователи"]
)

quizes_router = APIRouter(
    prefix="/quizzes",
    tags = ["Квизы"]
)

questions_router = APIRouter(
    prefix="/questions",
    tags = ["Вопросы"]
)

@default_router.get('/', tags=['API V1'])
async def index():
    return {'data': 'ok'}


@users_router.get('')
async def users_get() -> dict[str, list[User]|str]:
    users = await ur.get_users()
    return {'status':'ok', 'data':users}


@users_router.get('/{id}')
async def user_get(id: int) -> User:
    user = await ur.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="<User Not Found>")
    return user


@users_router.post('')
async def add_user(user: UserAdd = Depends()) -> UserId:
    id = await ur.add_user(user)
    return {'id':id}


@quizes_router.get('')
async def get_quizzes() -> dict[str, list[Quiz]|str]:
    quizes = await qz.get_quizzes()
    return {'status':'ok', 'data':quizes}


@quizes_router.get('/{id}')
async def get_quizz(id: int) -> Quiz:
    quiz = await qz.get_quiz(id)
    if not quiz:
        raise HTTPException(status_code=404, detail="<Quiz Not Found>")
    return quiz


@quizes_router.post('')
async def add_quiz(quiz: QuizAdd = Depends()) -> QuizId:
    id = await qz.add_quiz(quiz)
    return {'id':id}


@quizes_router.get('/{id}/questions')
async def get_quiz_questions(id: int) -> dict | QuizWithQuestions | list[Question]:
    quiz = await qz.get_quiz_with_questions(id)
    if not quiz:
        raise HTTPException(status_code=404, detail="<Quiz Not Found>")
    return QuizWithQuestions.model_validate(quiz)


@quizes_router.post('/{id}/link')
async def link_questions_to_quiz(
    id: int,
    payload: LinkQuestionsId
) -> dict:
    result = await qz.link_questions(id, payload.question_ids)
    if result.get("reason") == "quiz_not_found":
        raise HTTPException(status_code=404, detail="<Quiz Not Found>")

    return {"status": "ok", "result": result}


@questions_router.get('')
async def get_questions() -> dict[str, list[Question]|str]:
    questions = await qq.get_questions()
    return {'status':'ok', 'data':questions}


@questions_router.get('/{id}')
async def get_question(id: int) -> Question:
    question = await qq.get_question(id)
    if not question:
        raise HTTPException(status_code=404, detail="<Question Not Found>")
    return question


@questions_router.post('')
async def add_question(question: QuestionAdd = Depends()) -> QuestionId:
    id = await qq.add_question(question)
    return {'id':id}
