from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey

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


class UserOrm(Model):
    __tablename__ = 'users'
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str|None]
    # quiz = relationship('QuizOrm', backref='user')

class QuizOrm(Model):
    __tablename__ = 'quizes'
    name: Mapped[str]
    # user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # user = relationship('UserOrm', backref='quizes')

class QuestionOrm(Model):
    __tablename__ = 'questions'
    text: Mapped[str]
    answer: Mapped[str]
    wrong1: Mapped[str]
    wrong2: Mapped[str]
    wrong3: Mapped[str]