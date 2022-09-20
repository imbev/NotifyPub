import os
from sqlalchemy import create_engine, select, desc, insert
import flask
from flask import Blueprint, current_app, render_template, redirect, url_for, make_response, request
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from app.login import login_manager
from app.model import meta, messages, tokens

website = Blueprint('website', __name__)

engine = create_engine(os.getenv("DATABASE"), connect_args={'check_same_thread': False})
meta.create_all(engine)

@website.route("/")
def index():
    return render_template('index.html', config=current_app.config['WEBSITE'])

@website.route('/dashboard')
@login_required
def dashboard():
    with engine.begin() as conn:
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

class TokenForm(FlaskForm):
    description = StringField('description', validators=[DataRequired()])
    token = StringField('token', validators=[DataRequired()])
    submit = SubmitField('Submit')
@website.route('/manage_tokens', methods=['GET', 'POST'])
@login_required
def manage_tokens():
    form = TokenForm()
    error_message = ""
    with engine.begin() as conn:
        tokens_ = conn.execute(select(tokens).order_by(desc(tokens.c.time_created))).all()
    if form.validate_on_submit():
        description = form.data['description']
        token = form.data['token']
        with engine.begin() as conn:
            statement = insert(tokens).values(description=description, token=token)
            result = conn.execute(statement.compile())
        return flask.redirect(flask.url_for('website.index'))
    return render_template(
        'manage_tokens.html', 
        config=current_app.config['WEBSITE'],
        form=form,
        tokens=tokens_,
        error_message=error_message)

@website.route('/share', methods=['GET', 'POST'])
def share():
    token = request.args.get('token')
    matched = False
    with engine.begin() as conn:
        if not conn.execute(select(tokens).filter_by(token=token)).first():
            return 'Invalid Token', 401

    with engine.begin() as conn:
        published = conn.execute(select(messages).order_by(desc(messages.c.time_created))).all()
    template = render_template('share.xml', config=current_app.config['WEBSITE'], notifications=published, token=token)
    resp = make_response(template)
    resp.headers['Content-Type'] = 'application/xml'
    return resp