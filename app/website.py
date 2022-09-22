import os
from sqlalchemy import create_engine, select, desc, insert, delete
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
@website.route('/manage/notification', methods=['GET', 'POST'])
@login_required
def manage_notifications():
    form = NotificationForm()
    form_error_message = ""
    with engine.begin() as conn:
        notifications_ = conn.execute(select(messages).order_by(desc(messages.c.time_created))).all()
    if form.validate_on_submit():
        title = form.data['title']
        summary = form.data['summary']
        content = form.data['content']
        with engine.begin() as conn:
            statement = insert(messages).values(title=title, summary=summary, content=content)
            result = conn.execute(statement.compile())
        return flask.redirect(flask.url_for('website.dashboard'))
    return render_template(
        'manage_notifications.html', 
        config=current_app.config['WEBSITE'],
        form=form,
        notifications=notifications_,
        form_error_message=form_error_message,
        error_message=request.args.get('error_message'),
        success_message=request.args.get('success_message'))

class TokenForm(FlaskForm):
    description = StringField('description', validators=[DataRequired()])
    token = StringField('token', validators=[DataRequired()])
    submit = SubmitField('Submit')
@website.route('/manage/token', methods=['GET', 'POST'])
@login_required
def manage_tokens():
    form = TokenForm()
    with engine.begin() as conn:
        tokens_ = conn.execute(select(tokens).order_by(desc(tokens.c.time_created))).all()
    if form.validate_on_submit():
        description = form.data['description']
        token = form.data['token']
        with engine.begin() as conn:
            statement = insert(tokens).values(description=description, token=token)
            result = conn.execute(statement.compile())
        return flask.redirect(flask.url_for('website.dashboard'))
    return render_template(
        'manage_tokens.html', 
        config=current_app.config['WEBSITE'],
        form=form,
        tokens=tokens_,
        form_error_message=request.args.get('form_error_message'),
        error_message=request.args.get('error_message'),
        success_message=request.args.get('success_message'))

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

@website.route('/delete/token')
@login_required
def delete_token():
    token_id = request.args.get('token_id')
    with engine.begin() as conn:
        if not conn.execute(select(tokens).filter_by(id=token_id)).first():
            return redirect(url_for('website.manage_tokens', error_message=f'Invalid Token id: {token_id}'))
        else:
            token_desc = conn.execute(select(tokens).filter_by(id=token_id)).first()[2]
            conn.execute(delete(tokens).where(tokens.c.id == token_id))
            return redirect(url_for('website.manage_tokens', success_message=f"Successfully deleted token \"{token_desc}\"."))

@website.route('/delete/notification')
@login_required
def delete_notification():
    notification_id = request.args.get('notification_id')
    with engine.begin() as conn:
        if not conn.execute(select(messages).filter_by(id=notification_id)).first():
            return redirect(url_for('website.manage_notifications', error_message=f'Invalid Notification id: {notification_id}'))
        else:
            notification_title = conn.execute(select(messages).filter_by(id=notification_id)).first()[1]
            conn.execute(delete(messages).where(messages.c.id == notification_id))
            return redirect(url_for('website.manage_notifications', success_message=f"Successfully deleted notification \"{notification_title}\"."))