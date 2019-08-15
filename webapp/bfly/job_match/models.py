from bfly.db import db
from sqlalchemy import func, or_
from datetime import datetime
import bfly.users.models
import enum


class MatchStatus(enum.Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    done = 'done'


class MatchRequest(db.Model):
    __tablename__ = "match_request"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer)
    major = db.Column(db.String(255))
    requesting_user_id = db.Column(db.String(255)) # who needs a job?
    worker_id = db.Column(db.String(255)) # who is assigned to this?

    status = db.Column(db.String(10), default=MatchStatus.pending.value)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        import pdb; pdb.set_trace()
        return 'User: {}, Job: {}, Status: {}'.format(self.requesting_user_id, self.job_id, self.status)

    def to_dict(self):
        data = self.__dict__.copy()
        return data


def update_job_match(id, params):
    request = MatchRequest.query.get(id)
    if not request:
        raise ValueError("No user with that id")

    if 'id' in params:
        del params['id']

    for key, value in params.items():
        setattr(request, key, value)
    request.updated_on = datetime.utcnow()

    ret_dict = request.to_dict()
    db.session.add(request)
    db.session.commit()
    return ret_dict


def query_for_job_matches(user_id, worker_id, status):
    query = MatchRequest.query
    if user_id:
        query = query.filter(MatchRequest.requesting_user_id == user_id)
    if worker_id:
        query = query.filter(MatchRequest.worker_id == worker_id)
    if status:
        query = query.filter(MatchRequest.status == status)
    return query.all()


def create_tables():
    db.create_all()
    db.session.commit()


def initialize_data():
    recently_created_match = MatchRequest(
        job_id=1,
        major='Accounting',
        requesting_user_id='george@butterflyone.co',
    )
    recently_assigned_match = MatchRequest(
        job_id=3,
        major='Accounting',
        requesting_user_id='george@butterflyone.co',
        worker_id='diego@butterflyone.co',
        status=MatchStatus.in_progress.value
    )
    done_match = MatchRequest(
        job_id=4,
        major='Accounting',
        requesting_user_id='george@butterflyone.co',
        worker_id='andres@butterflyone.co',
        status=MatchStatus.done.value
    )
    db.session.add(recently_created_match)
    db.session.add(recently_assigned_match)
    db.session.add(done_match)

    db.session.commit()
