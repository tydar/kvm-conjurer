import os
import tempfile
import requests

import pytest
from conjurer import create_app
from conjurer.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

# Get a debian cloud image to use to test libvirt
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'images/debian10.qcow2')):
    image_url = 'https://cloud.debian.org/images/cloud/buster/20201214-484/debian-10-generic-amd64-20201214-484.qcow2'
    r = requests.get(image_url)

    with open(os.path.join(os.path.dirname(__file__), 'images/debian10.qcow2'), 'wb') as f:
        f.write(r.content)

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

"""
Create a wrapper class to be passed by pytest fixture
that implements auth for testing purposes in a DRY way
"""

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
