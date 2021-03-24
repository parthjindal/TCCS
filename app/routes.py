from flask.helpers import url_for
from app.forms import LoginForm
from app import app
from flask import flash, redirect,url_for,render_template
from .data import user,posts

@app.route('/')
def index():
    return "IGHT Imma Head out"


@app.route('/home')
def home():
    return render_template('index.html', title='TL;DR', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for user{form.username.data}")
        return redirect(url_for('home'))
    # if form.validate_on_submit():
    return render_template('login_form.html',title='Sign In',form = form)
