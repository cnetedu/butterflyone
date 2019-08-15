import bfly.db
import bfly.job_match.api
import bfly.job_match.models
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
        bfly.job_match.models.MatchRequest.__table__.create(bind=bfly.db.db.engine, checkfirst=False)


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


def test_create_dumb_job_match(test_client):
    post_result = test_client.post('/job_match/api', headers={"Content-Type": "application/json"}, json=dict(
        job_id="cool job id",
        requesting_user_id="george",
        major="Accounting"))
    assert '201' in post_result.status

    get_result = test_client.get('/job_match/api?request_user_id=george')
    assert '200' in get_result.status
    assert get_result.json[0]['job_id'] == 'cool job id'


def test_create_and_update_job_match(test_client):
    test_client.post('/job_match/api', headers={"Content-Type": "application/json"}, json=dict(
        job_id="cool job id",
        requesting_user_id="george",
        major="Accounting"))

    get_result = test_client.get('/job_match/api?request_user_id=george').json
    assert len(get_result) == 1
    assert get_result[0]['status'] == 'pending'

    put_result = test_client.put(
        '/job_match/api/{}'.format(get_result[0]['id']),
        headers={'Content-Type': 'application/json'},
        json=dict(status="in progress"))

    assert put_result.json['status'] == 'in progress'
