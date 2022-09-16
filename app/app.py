from flask import Flask
from dotenv import load_dotenv; load_dotenv()
import os

from app.website import website
from app.login import login_manager, login
from app.api import api

def create_app():
    app = Flask(__name__)

    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['WEBSITE'] = {
        'base_url': os.getenv('HOST'),
        'title': os.getenv('TITLE')
    }

    login_manager.init_app(app)
    

    app.register_blueprint(website)
    app.register_blueprint(login)
    app.register_blueprint(api, url_prefix='/api')

    return app