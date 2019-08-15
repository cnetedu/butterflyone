import bfly.db
import bfly.jobs.models
import bfly.majors.models
import bfly.server
import pytest
import os
import tempfile


class Config(object):
    def __init__(self, sql_file_path):
        self.SQLALCHEMY_DATABASE_URI = (
            'sqlite:///' + sql_file_path
        )

INSERT_MAJOR_DATA = """
INSERT INTO majors (title, best_job_1, best_job_2, best_job_3, best_jobs)
VALUES
  ('Accounting', 'Staff Accountant', 'Accountant', 'Office Manager', '["Staff Accountant", "Accountant", "Office Manager", "Accounting Clerk"]'),
  ('Animation', 'Animator', 'Graphic Designer', 'Artist', '["Animator", "Graphic Designer", "Artist", "3D Artist"]');

"""


INSERT_JOB_DATA = """
INSERT INTO jobs (title)
VALUES
  ('Accountant'),
  ('Office Manager');
"""


def init_db(app):
    with app.app_context():
        bfly.majors.models.Major.__table__.create(bind=bfly.db.db.engine, checkfirst=False)
        bfly.jobs.models.Job.__table__.create(bind=bfly.db.db.engine, checkfirst=False)
        bfly.db.db.engine.execute(INSERT_MAJOR_DATA)
        bfly.db.db.engine.execute(INSERT_JOB_DATA)


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


def test_get_majors(test_client):
    results = bfly.majors.models.list_majors()[0]
    assert len(results) == 2, "Expected 2 majors"
    accounting_dict = [r for r in results if r['title'] == 'Accounting'].pop()
    assert accounting_dict['best_jobs'] == '["Staff Accountant", "Accountant", "Office Manager", "Accounting Clerk"]'

    animation_dict = [r for r in results if r['title'] == 'Animation'].pop()
    assert animation_dict['best_jobs'] == '["Animator", "Graphic Designer", "Artist", "3D Artist"]'


def test_get_jobs(test_client):
    results = bfly.jobs.models.list_jobs()[0]
    assert len(results) == 2
    titles = [r['title'] for r in results]
    expected_titles = ['Accountant', 'Office Manager']
    for title in expected_titles:
        assert title in titles


def test_get_jobs_by_major(test_client):
    results = bfly.majors.models.list_jobs_by_majors(['Accounting'])[0]
    assert len(results) == 2
    expected_titles = ['Accountant', 'Office Manager']
    received_titles = [r['title'] for r in results]
    for title in expected_titles:
        assert title in received_titles


def test_crud_get_jobs(test_client):
    response = test_client.get('/jobs')
    assert response.status_code == 200

    assert response.json['jobs'] is not None
    assert len(response.json['jobs']) == 2
    titles = [r['title'] for r in response.json['jobs']]
    assert 'Accountant' in titles
    assert 'Office Manager' in titles


def test_crud_get_job(test_client):
    response = test_client.get('/jobs/1')
    assert response.status_code == 200

    assert response.json is not None
    assert response.json['title'] == 'Accountant'


def test_crud_get_majors(test_client):
    response = test_client.get('/majors')
    assert response.status_code == 200

    assert len(response.json['majors']) == 2
    titles = [m['title'] for m in response.json['majors']]
    assert 'Accounting' in titles
    assert 'Animation' in titles


def test_crud_get_major(test_client):
    response = test_client.get('/majors/Animation')
    assert response.status_code == 200

    assert response.json is not None
    assert response.json['title'] == 'Animation'
