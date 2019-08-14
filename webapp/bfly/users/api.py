from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_restplus import Api, Resource, fields
from werkzeug import secure_filename

import bfly.users.forms
import bfly.users.models
import flask
import random


users = Blueprint('users', __name__, template_folder="templates")
api = Api(users)
ns_conf = api.namespace('api', description="Users")


@users.route('/dashboard', methods=["GET"])
def dashboard():
    users, cursor = bfly.users.models.list_users(100, None)
    return render_template('users.html', title='Users', users=users)


@users.route('/upload', methods=['GET', 'POST'])
def creation():
    form = bfly.users.forms.UserCreation()

    if form.validate_on_submit():
        user = bfly.users.models.User(
            id=form.email.data,
            fullname=form.fullname.data,
            email=form.email.data,
            phone=form.phone.data,
            major=form.major.data,
            college=form.college.data,
            graduationMonth=form.graduationMonth.data,
            graduationYear=form.graduationYear.data,
            gpa=form.gpa.data,
            currentLocation=form.currentLocation.data,
            desiredLocation1=form.desiredLocation1.data,
            desiredLocation2=form.desiredLocation2.data,
            desiredLocation3=form.desiredLocation3.data,
        )

        bfly.users.models.db.session.add(user)
        bfly.users.models.db.session.commit()

        resume = bfly.users.models.Resume(
            data=form.binaryResume.data.stream.read(),
            name=form.binaryResume.data.name,
            content_type=form.binaryResume.data.content_type,
            id=user.id
        )
        bfly.users.models.db.session.add(resume)
        bfly.users.models.db.session.commit()

        flash("You successfully created a user.")
        return redirect(url_for("users.dashboard"))

    return render_template('user_creation.html', form=form, title="Create User")


user_model = api.model('User', {
    'id': fields.String,
    'fullname': fields.String,
    'phone': fields.String,
    'email': fields.String,
    'major': fields.String,
    'college': fields.String,
    'graduationMonth': fields.Integer,
    'graduationYear': fields.Integer,
    'gpa': fields.String,
    'currentLocation': fields.String,
    'desiredLocation1': fields.String,
    'desiredLocation2': fields.String,
    'desiredLocation3': fields.String
})

list_of_users = api.model("ListOfUsers", {
    'users': fields.List(fields.Nested(user_model)),
    'token': fields.String
})

user_update = api.model('UserUpdate', {
    'fullname': fields.String(),
    'major1': fields.String,
    'major2': fields.String,
    'major3': fields.String,
    'college': fields.String,
    'graduationMonth': fields.Integer,
    'graduationYear': fields.Integer
})

user_creation = api.model('UserCreation', {
    'fullname': fields.String,
    'phone': fields.String,
    'email': fields.String
})

@ns_conf.route('/<string:id>')
@ns_conf.response(404, 'User not found.')
class User(Resource):
    @ns_conf.marshal_with(user_model)
    def get(self, id):
        """
        Return a specific user
        :param id:
        :return:
        """
        user_dict = bfly.users.models.get_user(id)
        if user_dict:
            return user_dict, 200
        else:
            ns_conf.abort(404)

    @ns_conf.expect(user_update, validate=True)
    @ns_conf.marshal_with(user_model)
    def put(self, id):
        """
        Update a user
        :param id:
        :return:
        """
        try:
            bfly.users.models.update_user(id, request.json)
        except ValueError:
            ns_conf.abort(404)


@ns_conf.route('/resume/<string:id>')
class Resume(Resource):
    def get(self, id):
        resume_data = bfly.users.models.get_resume(id)
        if resume_data:
            response = flask.make_response(resume_data.data, 200)
            response.headers['content-type'] = resume_data.content_type
            return response
        else:
            ns_conf.abort(404)

    def put(self, id):
        pass


def validate_required_creation(data_dict):
    for key in ['fullname', 'phone', 'email']:
        if key not in data_dict:
            raise ValueError("{} required in data".format(key))


@ns_conf.route('')
class UserList(Resource):
    @ns_conf.marshal_list_with(list_of_users)
    def get(self):
        users, next_page = bfly.users.models.list_users()
        return dict(users=users, token=next_page), 200

    @ns_conf.expect(user_creation, validate=True)
    @ns_conf.response(201, "User created successfully")
    def post(self):
        """
        Creates a new user
        :return:
        """
        data = request.json
        if 'id' in data:
            del data['id']

        validate_required_creation(data)
        user = bfly.users.models.User(
            id=data['email'],
            fullname=data['fullname'],
            phone=data['phone'],
            email=data['email']
        )

        bfly.users.models.db.session.add(user)
        bfly.users.models.db.session.commit()
        return dict(status="Success"), 201
