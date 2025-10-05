from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

quiz_questions = db.Table(
    'quiz_questions',
    db.Column('quiz_id', db.Integer, db.ForeignKey('quizzes.id'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True),
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    quizzes = db.relationship('Quiz',
                             backref='user',
                             cascade='all, delete-orphan',
                             lazy='select')

    def __init__(self, name):
        super().__init__()
        self.name = name


    def __repr__(self):
        return f'<User id={self.id}, name = {self.name}>'

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='quizzes')

    questions = db.relationship(
        'Question',
        secondary=quiz_questions,
        backref='quizzes',
        lazy='select'
    )

    def __init__(self, name, user_id):
        super().__init__()
        self.name = name
        self.user_id = user_id


    def __repr__(self):
        return f'<Quiz id={self.id}, name = {self.name}>'


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    wrong1 = db.Column(db.String(100), nullable=False)
    wrong2 = db.Column(db.String(100), nullable=False)
    wrong3 = db.Column(db.String(100), nullable=False)

    quizzes = db.relationship('Quiz',
                             secondary=quiz_questions,
                             backref='questions',
                             lazy='select')


    def __init__(self, text, answer, wrong1, wrong2, wrong3):
        super().__init__()
        self.text = text
        self.answer = answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    def __repr__(self):
        return f'<Question id={self.id}, text = {self.text}>'