import os
from sqlalchemy import create_engine
from flask import Blueprint, current_app, render_template, redirect, url_for
from flask_login import login_required
from app.login import login_manager
from app.model import meta, messages, tokens

engine = create_engine(os.getenv("DATABASE"))
meta.create_all(engine)
conn = engine.connect()

website = Blueprint('website', __name__)

engine = create_engine(os.getenv("DATABASE"))
meta.create_all(engine)
conn = engine.connect()

@website.route("/")
def index():
    return render_template('index.html', config=current_app.config['WEBSITE'])

@website.route('/dashboard')
@login_required
def dashboard():
    published_count = 0
    tokens_count = 0
    return render_template(
        'dashboard.html',
         config=current_app.config['WEBSITE'], 
         published_count=published_count, 
         tokens_count=tokens_count
    )