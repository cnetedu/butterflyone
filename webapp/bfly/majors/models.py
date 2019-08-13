from bfly.db import db
import bfly.jobs.models

class Major(db.Model):
    __tablename__ = "majors"
    title = db.Column(db.String(255), primary_key=True)
    best_job_1 = db.Column(db.Text)
    best_job_2 = db.Column(db.Text)
    best_job_3 = db.Column(db.Text)
    best_jobs = db.Column(db.Text)

    def to_dict(self):
        data = self.__dict__.copy()
        data['title'] = self.title
        data.pop('_sa_instance_state')
        return data


def list_majors(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Major.query
             .order_by(Major.title)
             .limit(limit)
             .offset(cursor))
    majors = [m.to_dict() for m in query.all()]
    next_page = cursor + limit if len(majors) == limit else None
    return majors, next_page


def list_jobs_by_majors(majors, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    major_query = (Major.query
                   .filter(Major.title.in_(majors))
                   .order_by(Major.title))
    majors = major_query.all()

    jobs_to_return = []
    for major in majors:
        jobs_to_return.append(major.best_job_1)
        jobs_to_return.append(major.best_job_2)
        jobs_to_return.append(major.best_job_3)

    job_query = (bfly.jobs.models.Job.query
                 .filter(bfly.jobs.models.Job.title.in_(jobs_to_return))
                 .order_by(bfly.jobs.models.Job.title)
                 .limit(limit)
                 .offset(cursor))
    jobs = [j.to_dict() for j in job_query.all()]

    next_page = cursor + limit if len(jobs) == limit else None
    return jobs, next_page


def read_major(title):
    result = Major.query.get(title)
    if not result:
        return None
    return result.to_dict()
