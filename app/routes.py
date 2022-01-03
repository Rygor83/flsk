from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CarboForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/carbo', methods=['GET', 'POST'])
def carbo():
    form = CarboForm()
    amount = 0
    message = ""
    if form.validate_on_submit():
        if form.give_gramm.data and not form.give_xe.data:
            amount = float(form.give_gramm.data) * float(form.carbo_per_100g.data) / 100 / 12
            measure = 'XE'
            message = f"Results: {round(amount)} {measure}"
        elif form.give_xe.data and not form.give_gramm.data:
            amount = float(form.give_xe.data) * 12 * 100 / float(form.carbo_per_100g.data)
            measure = 'gramm'
            message = f"Results: {round(amount)} {measure}"
        elif form.give_xe.data and form.give_xe.data:
            message = f"Please fill in only one of the fields: either 'How much gramm will give' or 'How much XE will give'"
        elif not form.give_xe.data and not form.give_xe.data:
            message = f"Please fill in only one of the fields: either 'How much gramm will give' or 'How much XE will give'"
        flash(message)
    return render_template('carbo.html', title='Carbohydrates calculator', form=form)
