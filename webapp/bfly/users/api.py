from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_restplus import Api, Resource, fields
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from validate_email import validate_email

import bfly.users.forms
import bfly.users.models
import flask
import random
import phonenumbers

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
            usAuthorized=form.usAuthorized.data,
            over18=form.over18.data
        )

        bfly.users.models.db.session.add(user)
        bfly.users.models.db.session.commit()
        if form.binaryResume.data:
            resume = bfly.users.models.Resume(
                data=form.binaryResume.data.stream.read(),
                name=form.binaryResume.data.name,
                contentType=form.binaryResume.data.content_type,
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
    'desiredLocation3': fields.String,
    'usAuthorized': fields.Boolean,
    'over18': fields.Boolean,
})


list_of_users = api.model("ListOfUsers", {
    'users': fields.List(fields.Nested(user_model)),
    'token': fields.String
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

    @ns_conf.expect(user_model, validate=True)
    @ns_conf.marshal_with(user_model)
    def put(self, id):
        """
        Update a user
        :param id:
        :return:
        """
        try:
            return  bfly.users.models.update_user(id, request.json), 200
        except ValueError:
            ns_conf.abort(404)


@ns_conf.route('/resume/<string:id>')
class Resume(Resource):
    post_parser = ns_conf.parser()
    post_parser.add_argument('file', type=FileStorage, location="files")
    post_parser.add_argument('filename', type='string', location='form')

    def get(self, id):
        resume_data = bfly.users.models.get_resume(id)
        if resume_data:
            response = flask.make_response(resume_data.data, 200)
            response.headers['content-type'] = resume_data.contentType
            response.headers['filename'] = resume_data.name
            return response
        else:
            ns_conf.abort(404)

    @ns_conf.expect(post_parser, validate=True)
    def post(self, id):
        file = request.files['file']
        resume = bfly.users.models.get_resume(id)
        if resume:
            resume.data = file.read()
            resume.name = file.filename
            resume.contentType = file.content_type
        else:
            resume = bfly.users.models.Resume(
                data=file.read(),
                name=file.filename,
                contentType=file.content_type,
                id=id)

        bfly.users.models.db.session.add(resume)
        bfly.users.models.db.session.commit()
        return {"status": "success"}, 201


def validate_phone_number(phone_number):
    try:
        input_number = phonenumbers.parse(phone_number)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValueError('Invalid phone number.')
    except:
        input_number = phonenumbers.parse("+1"+phone_number)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValueError('Invalid phone number.')


def validate_fullname(name):
    if len(name) < 1:
        raise ValueError("Need something in name")


def validate_email_address(email):
    if not validate_email(email):
        raise ValueError("{} is not a valid email".format(email))


def validate_required_creation(data_dict):
    for key in ['fullname', 'phone', 'email']:
        if key not in data_dict:
            raise ValueError("{} required in data".format(key))

    validate_phone_number(data_dict['phone'])
    validate_email_address(data_dict['email'])
    validate_fullname(data_dict['fullname'])


@ns_conf.route('')
class UserList(Resource):
    @ns_conf.marshal_list_with(list_of_users)
    def get(self):
        users, next_page = bfly.users.models.list_users()
        return dict(users=users, token=next_page), 200

    @ns_conf.expect(user_creation, validate=True)
    @ns_conf.marshal_with(user_model, "User created successfully")
    def post(self):
        """
        Creates a new user
        :return:
        """
        data = request.json
        if 'id' in data:
            del data['id']

        try:
            validate_required_creation(data)
        except ValueError as exception:
            ns_conf.abort(400, "Issue with input data: {}".format(exception))

        user = bfly.users.models.User(
            id=data['email'],
            fullname=data['fullname'],
            phone=data['phone'],
            email=data['email']
        )

        bfly.users.models.db.session.add(user)
        d = user.to_dict()
        bfly.users.models.db.session.commit()
        return d, 201
