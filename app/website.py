from flask import Blueprint, current_app, render_template, redirect, url_for
from flask_login import login_required
from app.login import login_manager

website = Blueprint('website', __name__)

@website.route("/")
def index():
    return render_template('index.html', config=current_app.config['WEBSITE'])

