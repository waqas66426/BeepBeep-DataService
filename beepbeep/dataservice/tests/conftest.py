import pytest
import os
from beepbeep.dataservice.app import create_app
from beepbeep.dataservice.database import db as _db, init_database
import subprocess

# The scope of this instance is per-file
@pytest.fixture(scope="module")
def app():
    _app = create_app()
    yield _app
    print("\nApp shutted down...")

# The scope of this instance is per-file
@pytest.fixture(scope="module")
def db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" # in memory db for tests
    _db.init_app(app)
    _db.create_all(app=app)
    with app.app_context():
        init_database()
        yield _db
        
# The scope of this instance is per-file
@pytest.fixture(scope="module")
def client(app):
    client = app.test_client()

    yield client

