import pytest
from flask import url_for
import sys, os; sys.path.append(os.getcwd())
from app.app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

def test_ping(client):
    resp = client.get(url_for('api.ping'))
    assert resp.json == {'ping':'pong'}


