from flask import Blueprint, request, jsonify
import bfly.jobs.models

jobs = Blueprint('jobs', __name__)


@jobs.route("/jobs")
def list_jobs():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')


    jobs, next_page_token = bfly.jobs.models.list_jobs(cursor=token)

    return jsonify(dict(jobs=jobs, page_token=next_page_token))


@jobs.route('/jobs/<title>')
def view_job(title):
    job = bfly.jobs.models.read_job(title)
    return jsonify(job)
