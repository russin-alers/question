from flask.ext.login import LoginManager
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from app import app
#db configurations

# connecting to DB
import os
engine = create_engine('sqlite:///' + os.path.dirname(app.root_path) +
                       '/questions.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# using declarative method
Base = declarative_base()
Base.query = db_session.query_property()

# login settings
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)
    asked_questions = relationship('Questions')
    answers = relationship('Answers')

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %s>' % self.name

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    details = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    answers = relationship('Answers')

    def __init__(self, details, question, user_id):
        self.details = details
        self.question = question
        self.user_id = user_id

    def get_user(self):
        return User.query.filter_by(id=self.user_id).first().name


class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    answer = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)

    def __init__(self, answer, user_id, question_id):
        self.answer = answer
        self.user_id = user_id
        self.question_id = question_id

    def get_user(self):
        return User.query.filter_by(id=self.user_id).first().name


# decelerating models
def init_db():
    Base.metadata.create_all(bind=engine)

