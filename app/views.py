from flask import render_template, url_for, flash, request, redirect, g
from flask.ext.login import login_user, logout_user, login_required
from app.forms import AddQuestionForm, LoginForm, AnswerForm
from app.models import Questions, Answers, User, db_session, login_manager
from app import app

@app.route('/')
def index():
    return render_template('index.html', title='Question Test')


@app.route('/index')
def main_page():
    questions = Questions.query.all()
    return render_template('main.html', title='Question Test',
                           questions=questions)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_question():
    form = AddQuestionForm()
    if request.method == 'POST' and form.validate():
        user_id = g.user.id
        question = request.form['question']
        details = request.form['details']
        new_question = Questions(question=question, details=details,
                                 user_id=user_id)
        db_session.add(new_question)
        db_session.commit()
        flash('Your question successfully submitted!')
        return redirect(url_for('main_page'))
    return render_template('add_question.html', title='Add question', form=form)



@app.route('/answer/<question_id>', methods=['GET', 'POST'])

def answer(question_id):
    form = AnswerForm()
    question = Questions.query.filter_by(id=question_id).first()
    if not question:
        flash('Looks like this question is not available')
        return redirect(url_for('main_page'))
    if request.method == 'POST' and form.validate():
        answer_text = request.form['answer']
        user = g.user.id
        answer = Answers(answer_text, user, question.id)
        db_session.add(answer)
        db_session.commit()
        flash('Your answer successfully added')
        return redirect(url_for('main_page'))
    return render_template('answers.html', title='Answers',
                           question=question, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if g.user.is_authenticated():
        return redirect(url_for('main_page'))

    if request.method == 'POST':
        # login and validate the user...
        if form.validate():
            name = request.form['name']
            password = request.form['password']
            user = User.query.filter_by(name=name, password=password).first()
            if user is None:
                flash('Wrong data, try again')
                return redirect(url_for('login'))
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for('main_page'))
    return render_template("login_form.html", form=form, title='Log In')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if g.user.is_authenticated():
        return redirect(url_for('main_page'))

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        password = request.form['password']
        if not User.query.filter_by(name=name).first():
            user = User(name, password)
            db_session.add(user)
            db_session.commit()
            flash("You have successfully registered. Now you can log in.")
            return redirect(url_for('login'))
        else:
            flash('This name already used. Please try again.')
            return render_template('login_form.html',
                                   form=form,
                                   title='Sign up')
    return render_template('login_form.html', form=form, title='Register')


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out.')
    return redirect(url_for('main_page'))


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))