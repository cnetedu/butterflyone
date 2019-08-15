import bfly.db
import bfly.users.api
import bfly.users.models
import bfly.server
import pytest
import os
import tempfile

from io import BytesIO

class Config(object):
    def __init__(self, sql_file_path):
        self.SQLALCHEMY_DATABASE_URI = (
            'sqlite:///' + sql_file_path
        )


def init_db(app):
    with app.app_context():
        bfly.users.models.User.__table__.create(bind=bfly.db.db.engine, checkfirst=False)
        bfly.users.models.Resume.__table__.create(bind=bfly.db.db.engine, checkfirst=False)


@pytest.fixture()
def test_client():
    # Create temporary file for sqlite database.
    db_file_descriptor, path = tempfile.mkstemp()

    # Use config to point at sqlite database.
    test_config = Config(path)

    # Get instance of application
    flask_app = bfly.server.create_app(test_config, True, True)

    # Initialize sqlite database with stub data.
    init_db(flask_app)
    testing_client = flask_app.test_client()

    # Need to provide the application context to the usages of the testing_client.
    # I hate flask and should figure out how we can pass around an instance that isn't so "magic"
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

    # Clean up.
    os.close(db_file_descriptor)
    os.unlink(path)


def test_create_dumb_user(test_client):
    post_result = test_client.post('/users/api', headers={"Content-Type": "application/json"}, json=dict(
        email="george@butterflyone.co",
        fullname="george sequeira",
        phone="3016936356"))
    assert '201' in post_result.status

    get_result = test_client.get('/users/api/george@butterflyone.co')
    assert '200' in get_result.status
    assert get_result.json['id'] == 'george@butterflyone.co'
    assert get_result.json['fullname'] == 'george sequeira'


def test_validator_phone_number(test_client):
    assert bfly.users.api.validate_phone_number('3016936356') is None
    with pytest.raises(ValueError):
        bfly.users.api.validate_phone_number("9648436")


def test_validator_email(test_client):
    assert bfly.users.api.validate_email_address("george@butterflyone.co") is None
    with pytest.raises(ValueError):
        bfly.users.api.validate_email_address("9648436")


def test_create_and_update_user(test_client):
    test_client.post('/users/api', headers={"Content-Type": "application/json"}, json=dict(
        email="george@butterflyone.co",
        fullname="george sequeira",
        phone="3016936356"))

    get_result = test_client.get('/users/api/george@butterflyone.co')
    assert get_result.json['id'] == 'george@butterflyone.co'
    assert get_result.json['fullname'] == 'george sequeira'

    put_result = test_client.put(
        '/users/api/george@butterflyone.co',
        headers={'Content-Type': 'application/json'},
        json=dict(fullname="New George"))

    assert put_result.json['fullname'] == 'New George'
    get_result = test_client.get('/users/api/george@butterflyone.co')
    assert get_result.json['fullname'] == 'New George'


def test_upload_resume(test_client):
    resp = test_client.post('/users/api/resume/george@bfly.co', data={
        "file": (BytesIO(b"George's Resume"), 'resume.txt')},
        content_type='multipart/form-data')
    assert '201' in resp.status

    get_resp = test_client.get('/users/api/resume/george@bfly.co')
    assert b"George's Resume" == get_resp.data


def test_update_resume(test_client):
    resp = test_client.post('/users/api/resume/george@bfly.co', data={
        "file": (BytesIO(b"George's Resume"), 'resume.txt')},
        content_type='multipart/form-data')
    assert '201' in resp.status

    update_resp = test_client.post('/users/api/resume/george@bfly.co', data={
        "file": (BytesIO(b"George's New Resume"), 'resume.txt')},
        content_type='multipart/form-data')
    assert '201' in update_resp.status

    get_resp = test_client.get('/users/api/resume/george@bfly.co')
    assert b"George's New Resume" == get_resp.data
