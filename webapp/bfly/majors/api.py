from flask import Blueprint, request, jsonify
import bfly.majors.models

majors = Blueprint('majors', __name__)


@majors.route("/jobs_by_majors")
def list_jobs_for_major():
    token = request.args.get('page_token', None)
    majors = request.args.getlist('majors')

    if token:
        token = token.encode('utf-8')

    jobs, next_page_token = bfly.majors.models.list_jobs_by_majors(majors=majors, cursor=token)
    return jsonify(dict(jobs=jobs, page_token=next_page_token))


@majors.route("/majors")
def list_majors():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    majors, next_page_token = bfly.majors.models.list_majors(cursor=token)

    return jsonify(dict(majors=majors, page_token=next_page_token))


@majors.route('/majors/<title>')
def view_major(title):
    major = bfly.majors.models.read_major(title)
    return jsonify(major)
