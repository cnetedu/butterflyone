from bfly.db import db


class Job(db.Model):
    __tablename__ = "jobs"
    title = db.Column(db.String(255), primary_key=True)
    top_skills = db.Column(db.JSON)
    work_styles = db.Column(db.JSON)
    avg_salary = db.Column(db.Integer)
    description = db.Column(db.Text)
    duties = db.Column(db.Text)
    # industry = db.Column(db.Text)
    how_to_become = db.Column(db.Text)
    education = db.Column(db.Text)
    licenses = db.Column(db.Text)
    qualities = db.Column(db.Text)
    advancement = db.Column(db.Text)
    avg_length_of_employment_yr = db.Column(db.Float)
    majors = db.Column(db.Text)
    degrees = db.Column(db.Text)
    skills = db.Column(db.Text)
    other_skills = db.Column(db.Text)
    top_employers = db.Column(db.Text)
    career_path = db.Column(db.Text)

    def to_dict(self):
        data = self.__dict__.copy()
        data['title'] = self.title
        data.pop('_sa_instance_state')
        return data

    def __repr__(self):
        return "<Job (title='%s', salary='%s')" % (self.title, self.avg_salary)


def list_jobs(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Job.query
             .order_by(Job.title)
             .limit(limit)
             .offset(cursor))
    jobs = [j.to_dict() for j in query.all()]
    next_page = cursor + limit if len(jobs) == limit else None
    return jobs, next_page


def read_job(title):
    result = Job.query.get(title)
    if not result:
        return None
    return result.to_dict()


class JobListing(db.Model):
    __tablename__ = "job_listings"
    jobKey = db.Column(db.String(255), nullable=False, primary_key=True)
    source = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    jobTitle = db.Column(db.String(255))
    company = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    url = db.Column(db.String(255))
    snippet = db.Column(db.String(255))
    indeedApply = db.Column(db.Boolean)
    coverLetter =db.Column(db.Boolean)
    questions = db.Column(db.Text)


def list_job_listings(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (JobListing.query
             .order_by(JobListing.created)
             .limit(limit)
             .cursor(cursor))
    job_listings = [jl.to_dict() for jl in query.all()]
    next_page = cursor + limit if len(job_listings) == limit else None
    return job_listings, next_page


def read_job_listing(jobKey):
    result = JobListing.query.get(jobKey)
    if not result:
        return None
    return result.to_dict()
