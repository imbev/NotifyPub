from flask import Flask
from dotenv import load_dotenv; load_dotenv()
import os


HOST = os.getenv('HOST')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
DATABASE = os.getenv('DATABASE')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from app.model import db
    db.init_app(app)

    @app.route("/")
    def hello_world():
        return f"<p>Hello, welcome to {HOST}</p>"
    return app