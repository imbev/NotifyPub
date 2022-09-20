import flask
from flask import Blueprint, redirect, url_for, current_app, render_template
from flask_login import LoginManager, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class User:
    def __init__(self):
        self.password = ''

    def is_authenticated(self):
        if self.password == current_app.config['ADMIN_PASSWORD']:
            return True

    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return 'admin'
    def get(self, userid):
        return self

login = Blueprint('login', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get(User(), user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login.login_'))

@login.route("/login", methods=['GET', 'POST'])
def login_():
    form = LoginForm()
    error_message = ''
    if form.validate_on_submit():
        user = User.get(User(), 'admin')
        user.password = form.data['password']
        if user.is_authenticated():
            login_user(user)
            return flask.redirect(flask.url_for('website.dashboard'))
        error_message = 'Incorrect Password'
    return render_template('login.html', config=current_app.config['WEBSITE'], form=form, error_message=error_message)

@login.route("/logout")
def logout():
    user = User.get(User(), 'admin')
    logout_user()
    return flask.redirect(flask.url_for('website.index'))