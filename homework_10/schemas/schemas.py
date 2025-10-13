from pydantic import BaseModel, ConfigDict
from typing import List

class UserAdd(BaseModel):
    name: str
    age: int
    phone: str | None = None


class User(UserAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserId(BaseModel):
    id: int


class QuizAdd(BaseModel):
    name: str
    # user_id: int | None = None

class Quiz(QuizAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)

class QuizId(BaseModel):
    id: int


class QuestionAdd(BaseModel):
    text: str
    answer: str
    wrong1: str
    wrong2: str
    wrong3: str


class Question(QuestionAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class QuestionId(BaseModel):
    id: int


class LinkQuestionsId(BaseModel):
    question_ids: List[int]


class QuizWithQuestions(Quiz):
    questions: list[Question] = []
    model_config = ConfigDict(from_attributes=True)