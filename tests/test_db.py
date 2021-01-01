import sqlite3
import pytest
from conjurer.db import get_db

"""
Within the app_context, get_db should be idempotent and the connection
should be closed outside of the context
"""
def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raisers(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

"""
init-db cli should call init_db and output a message.
uses monkeypatch, the pytest fixture for mocking.
"""
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('conjurer.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
