from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, Table, Column

from datetime import datetime

class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    dateCreated: Mapped[datetime] = mapped_column(
                                            server_default=func.now(),
                                            nullable=False)
    dateModified: Mapped[datetime] = mapped_column(
                                            server_default=func.now(),
                                            server_onupdate=func.now(),
                                            nullable=False)


quiz_question_link = Table(
    "quiz_question_link",
    Model.metadata,
    Column("quiz_id", ForeignKey("quizes.id"), primary_key=True),
    Column("question_id", ForeignKey("questions.id"), primary_key=True),
)

class UserOrm(Model):
    __tablename__ = 'users'
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str|None]


class QuizOrm(Model):
    __tablename__ = 'quizes'
    name: Mapped[str]
    questions: Mapped[list["QuestionOrm"]] = relationship(
        secondary=quiz_question_link,
        back_populates="quizzes",
        lazy="selectin",
    )


class QuestionOrm(Model):
    __tablename__ = 'questions'
    text: Mapped[str]
    answer: Mapped[str]
    wrong1: Mapped[str]
    wrong2: Mapped[str]
    wrong3: Mapped[str]
    quizzes: Mapped[list["QuizOrm"]] = relationship(
        secondary=quiz_question_link,
        back_populates="questions",
        lazy="selectin",
    )