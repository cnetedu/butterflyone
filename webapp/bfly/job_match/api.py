from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_restplus import Api, Resource, fields
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from validate_email import validate_email

import bfly.job_match.models
import flask
import random
import phonenumbers

job_match = Blueprint('', __name__, template_folder="templates")
api = Api(job_match)
ns_conf = api.namespace('api', description="Job Match")


job_match_model = api.model('JobMatch', {
    'id': fields.Integer,
    'job_id': fields.String,
    'major': fields.String,
    'requesting_user_id': fields.String,
    'worker_id': fields.String,
    'status': fields.String,
    'created_on': fields.DateTime,
    'updated_on': fields.DateTime
})

job_match_creation = api.model('JobMatchCreation', {
    'job_id': fields.String,
    'requesting_user_id': fields.String,
    'major': fields.String
})


job_match_update = api.model('JobMatchUpdate', {
    'worker_id': fields.String,
    'status': fields.String
})


@ns_conf.route('')
class JobMatch(Resource):
    @ns_conf.expect(job_match_creation, validate=True)
    @ns_conf.marshal_with(job_match_model, "User created successfully")
    @ns_conf.response(404, 'Job or User not found')
    @ns_conf.response(201, 'JobMatch request made')
    def post(self):
        data = request.json
        job_match_obj = bfly.job_match.models.MatchRequest(
            job_id=data['job_id'],
            major=data['major'],
            requesting_user_id=data['requesting_user_id']
        )

        bfly.users.models.db.session.add(job_match_obj)
        d = job_match_obj.to_dict()
        bfly.users.models.db.session.commit()
        return d, 201

    @ns_conf.marshal_list_with(job_match_model)
    @ns_conf.doc(params={'request_user_id': 'users id', 'worker_id': 'who is working on it if necessary', 'status': 'what status do you want to check'})
    def get(self):
        parser = ns_conf.parser()
        parser.add_argument('request_user_id')
        parser.add_argument('worker_id')
        parser.add_argument('status')
        the_args = parser.parse_args()
        request_user_id = the_args.get('request_user_id')
        worker_id = the_args.get('worker_id')
        status = the_args.get('status')

        if not (request_user_id, worker_id, status):
            ns_conf.abort(400, "Need either request_user_id or worker_id or status")
        return bfly.job_match.models.query_for_job_matches(user_id=request_user_id, worker_id=worker_id, status=status), 200


@ns_conf.route('/<int:id>')
class JobMatchUpdate(Resource):
    @ns_conf.expect(job_match_update, validate=True)
    @ns_conf.marshal_with(job_match_model)
    def put(self, id):
        try:
            return  bfly.job_match.models.update_job_match(id, request.json), 200
        except ValueError:
            ns_conf.abort(404)


