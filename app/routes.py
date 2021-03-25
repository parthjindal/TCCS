from flask.blueprints import Blueprint
from flask_login import login_required
from flask import render_template
from .data import user,posts


main = Blueprint("main",import_name= __name__,template_folder="templates")

@main.route('/')
def index():
    return "IGHT Imma Head out"

@main.route('/home')
@login_required
def home():
    return render_template('index.html', title='TL;DR', user=user, posts=posts)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is not None:
#             print("hersabbbbbdddddddddddddddddddddddddddder\n\n\n\n\n\n")
#         if user is None or not user.check_password(form.password.data):
#             flash(f"Login requested for user{form.username.data}")
#             return redirect(url_for('index'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('home')
#         return redirect(next_page)
#     # if form.validate_on_submit():
#     return render_template('login_form.html', title='Sign In', form=form)


