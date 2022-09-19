import os
from sqlalchemy import create_engine, select, desc, insert
import flask
from flask import Blueprint, current_app, render_template, redirect, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from app.login import login_manager
from app.model import meta, messages, tokens

engine = create_engine(os.getenv("DATABASE"))
meta.create_all(engine)
conn = engine.connect()

website = Blueprint('website', __name__)

engine = create_engine(os.getenv("DATABASE"), connect_args={'check_same_thread': False})
meta.create_all(engine)
conn = engine.connect()

@website.route("/")
def index():
    return render_template('index.html', config=current_app.config['WEBSITE'])

@website.route('/dashboard')
@login_required
def dashboard():
    published = conn.execute(select(messages).order_by(desc(messages.c.time_created))).all()
    tokens_created = conn.execute(select(tokens).order_by(desc(tokens.c.time_created))).all()
    recent_published = published[0] if published else ""
    recent_token = tokens_created[0] if tokens_created else ""
    return render_template(
        'dashboard.html',
         config=current_app.config['WEBSITE'], 
         published_count=len(published), 
         tokens_count=len(tokens_created),
         recent_published=recent_published,
         recent_token=recent_token
    )

class NotificationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('summary', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('Submit')
@website.route('/new_notification', methods=['GET', 'POST'])
@login_required
def new_notification():
    form = NotificationForm()
    error_message = ""
    if form.validate_on_submit():
        title = form.data['title']
        summary = form.data['summary']
        content = form.data['content']
        with engine.begin() as conn:
            statement = insert(messages).values(title=title, summary=summary, content=content)
            result = conn.execute(statement.compile())
        return flask.redirect(flask.url_for('website.index'))
    return render_template(
        'new_notification.html', 
        config=current_app.config['WEBSITE'],
        form=form,
        error_message=error_message)