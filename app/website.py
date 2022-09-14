from flask import Blueprint, current_app

website_blueprint = Blueprint('website_blueprint', __name__)

@website_blueprint.route("/")
def hello_world():
    return f"<p>Hello, welcome to {current_app.config['HOST']}</p>"