from flask import Flask
from dotenv import load_dotenv; load_dotenv()
import os

from app.website import website_blueprint
from app.login import login_manager, login_blueprint
from app.model import db


def create_app():
    app = Flask(__name__)

    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{os.getenv("DATABASE")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['WEBSITE'] = {
        'base_url': os.getenv('HOST'),
        'title': os.getenv('TITLE')
    }

    db.init_app(app)
    login_manager.init_app(app)
    

    app.register_blueprint(website_blueprint)
    app.register_blueprint(login_blueprint)

    return app