from flask import Flask
from dotenv import load_dotenv; load_dotenv()
import os


HOST = os.getenv('HOST')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def hello_world():
        return f"<p>Hello, welcome to {HOST}</p>"
    return app