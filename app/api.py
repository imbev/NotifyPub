import os
from sqlalchemy import create_engine
from flask import jsonify, current_app, Blueprint
from app.model import meta, messages, tokens

engine = create_engine(os.getenv("DATABASE"))
meta.create_all(engine)
conn = engine.connect()

api = Blueprint('api', __name__)

@api.route('/ping')
def ping():
    return jsonify({'ping':'pong'})