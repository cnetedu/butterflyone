from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_restplus import Api, Resource, fields
import bfly.users.forms
import bfly.users.models
import random


users = Blueprint('users', __name__, template_folder="templates")
api = Api(users)
ns_conf = api.namespace('users', description="Users")

@users.route('/dashboard', methods=["GET"])
def dashboard():
    users, cursor = bfly.users.models.list_users(10, None)
    return render_template('users.html', title='Users', users=users)


@users.route('/creation', methods=['GET', 'POST'])
def creation():
    form = bfly.users.forms.UserCreation()
    if form.validate_on_submit():
        user = bfly.users.models.User(
            id="{}".format(random.randint(1,10000)),
            fullname=form.fullname.data,
            email=form.email.data,
            major1=form.major1.data,
            major2=form.major2.data,
            major3=form.major3.data,
            college=form.college.data,
            graduationMonth=form.graduationMonth.data,
            graduationYear=form.graduationYear.data,
        )

        bfly.users.models.db.session.add(user)
        bfly.users.models.db.session.commit()
        flash("You successfully created a user.")
        return redirect(url_for("users.dashboard"))

    return render_template('user_creation.html', form=form, title="Create User")


user_model = api.model('User', {
    'id': fields.String,
    'fullname': fields.String,
    'email': fields.String,
    'major1': fields.String,
    'major2': fields.String,
    'major3': fields.String,
    'college': fields.String,
    'graduationMonth': fields.Integer,
    'graduationYear': fields.Integer
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


@ns_conf.route('')
class UserList(Resource):
    @ns_conf.marshal_list_with(user_model)
    def get(self):
        return bfly.users.models.list_users(), 200

    @ns_conf.expect(user_model, validate=True)
    @ns_conf.response(201, "User created successfully")
    def post(self):
        """
        Creates a new user
        :return:
        """
        data = request.json
        if 'id' in data:
            del data['id']

        user = bfly.users.models.User(
            id="{}".format(random.randint(1,10000)),
            fullname=data['fullname'],
            email=data['email'],
            major1=data.get('major1', ''),
            major2=data.get('major2', ''),
            major3=data.get('major3', ''),
            college=data.get('college', ''),
            graduationMonth=data.get('graduationMonth', '5'),
            graduationYear=data.get('graduationYear', '2021'),
        )

        bfly.users.models.db.session.add(user)
        bfly.users.models.db.session.commit()
        return dict(status="Success"), 201
