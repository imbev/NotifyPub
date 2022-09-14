from flask import Flask
from dotenv import load_dotenv; load_dotenv()
import os

from app.website import website_blueprint


def create_app():
    app = Flask(__name__)

    app.config['HOST'] = os.getenv('HOST')
    app.config['ADMIN_PASSWORD'] = os.getenv('ADMIN_PASSWORD')
    app.config['DATABASE'] = os.getenv('DATABASE')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.config["DATABASE"]}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from app.model import db
    db.init_app(app)

    app.register_blueprint(website_blueprint)

    return app