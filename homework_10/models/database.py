from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

from .models import UserOrm, Model, QuizOrm, QuestionOrm
from schemas.schemas import *

import os



BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, 'fastapi.db')

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)

    @classmethod
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Model.metadata.drop_all)

    @classmethod
    async def add_test_data(cls):
        async with new_session() as session:
            users = [
                UserOrm(name='user1', age=20),
                UserOrm(name='user2', age=30, phone='123456789'),
                UserOrm(name='user3', age=41, phone='11'),
                UserOrm(name='user4', age=42, phone='22'),
                UserOrm(name='user5', age=43, phone='33'),
                UserOrm(name='user6', age=44),
                UserOrm(name='user7', age=45)
            ]
            session.add_all(users)
            await session.flush()
            quizzes = [
                QuizOrm(name='quiz1'),
                QuizOrm(name='quiz2'),
                QuizOrm(name='quiz3'),
            ]
            session.add_all(quizzes)
            await session.flush()

            questions = [
                QuestionOrm(text='Сколько будут 2+2*2',
                            answer='6',
                            wrong1='8',
                            wrong2='2',
                            wrong3='0',),
                QuestionOrm(text='Сколько месяцев в году имеют 28 дней?',
                            answer='Все',
                            wrong1='Один',
                            wrong2='Ни одного',
                            wrong3='Два'),
                QuestionOrm(text='Каким станет зелёный утёс, если упадет в Красное море?',
                            answer='Мокрым?',
                            wrong1='Красным',
                            wrong2='Не изменится',
                            wrong3='Фиолетовым'),
                QuestionOrm(text='Какой рукой лучше размешивать чай?',
                            answer='Ложкой',
                            wrong1='Правой',
                            wrong2='Левой',
                            wrong3='Любой')
            ]
            session.add_all(questions)
            await session.flush()
            await session.commit()

class UserRepository:
    @classmethod
    async def add_user(cls, user = UserAdd) -> int:
        async with new_session() as session:
            data = user.model_dump()
            user = UserOrm(**data)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id


    @classmethod
    async def get_users(cls) -> list[UserOrm]:
        async with new_session() as session:
            query = select(UserOrm)
            res = await session.execute(query)
            users = res.scalars().all()
            return users

    @classmethod
    async def get_user(cls, id: int) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == id)
            res = await session.execute(query)
            user = res.scalars().first()
            return user

class QuizRepository:
    @classmethod
    async def add_quiz(cls, quiz: QuizAdd) -> int:
        async with new_session() as session:
            data = quiz.model_dump()
            quiz = QuizOrm(**data)
            session.add(quiz)
            await session.flush()
            await session.commit()
            return quiz.id

    @classmethod
    async def get_quizzes(cls) -> list[QuizOrm]:
        async with new_session() as session:
            query = select(QuizOrm)
            res = await session.execute(query)
            quizzes = res.scalars().all()
            return quizzes

    @classmethod
    async def get_quiz(cls, id: int) -> QuizOrm:
        async with new_session() as session:
            query = select(QuizOrm).where(QuizOrm.id == id)
            res = await session.execute(query)
            quiz = res.scalars().first()
            return quiz

    @classmethod
    async def get_quiz_with_questions(cls, id: int) -> QuizOrm | None:
        async with new_session() as session:
            query = (
                select(QuizOrm)
                .options(selectinload(QuizOrm.questions))
                .where(QuizOrm.id == id)
            )
            res = await session.execute(query)
            return res.scalars().first()

    @classmethod
    async def link_questions(cls, quiz_id: int, question_ids: list[int]) -> dict:
        async with new_session() as session:
            quiz = await session.get(QuizOrm, quiz_id, options=[selectinload(QuizOrm.questions)])
            if not quiz:
                return {"ok": False, "reason": "quiz_not_found"}
            if not question_ids:
                return {"ok": True, "added": [], "skipped": [], "missing": []}

            q = select(QuestionOrm).where(QuestionOrm.id.in_(question_ids))
            res = await session.execute(q)
            existing_questions = res.scalars().all()
            existing_ids = {q.id for q in existing_questions}
            missing = [qid for qid in set(question_ids) if qid not in existing_ids]

            current_ids = {q.id for q in quiz.questions}
            to_add = [q for q in existing_questions if q.id not in current_ids]
            skipped = [q.id for q in existing_questions if q.id in current_ids]

            if to_add:
                quiz.questions.extend(to_add)
                await session.flush()
            await session.commit()
            return {
                "ok": True,
                "added": [q.id for q in to_add],
                "skipped": skipped,
                "missing": missing,
            }

class QuestionRepository:
    @classmethod
    async def add_question(cls, question: QuestionAdd) -> int:
        async with new_session() as session:
            data = question.model_dump()
            question = QuestionOrm(**data)
            session.add(question)
            await session.flush()
            await session.commit()
            return question.id

    @classmethod
    async def get_questions(cls) -> list[QuestionOrm]:
        async with new_session() as session:
            query = select(QuestionOrm)
            res = await session.execute(query)
            questions = res.scalars().all()
            return questions

    @classmethod
    async def get_question(cls, id: int) -> QuestionOrm:
        async with new_session() as session:
            query = select(QuestionOrm).where(QuestionOrm.id == id)
            res = await session.execute(query)
            question = res.scalars().first()
            return question

