from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

import bfly.users.models
import os
import phonenumbers

script_dir = os.path.dirname(__file__)
majors_rel_path = 'list_of_majors.txt'
majors = []
with open(os.path.join(script_dir, majors_rel_path)) as o:
    for line in o:
        majors.append(line.strip())

cities_rel_path = "list_of_cities.txt"
cities = []
with open(os.path.join(script_dir, cities_rel_path)) as o:
    for line in o:
        cities.append(line.strip())

universities_rel_path = "list_of_universities.txt"
universities = []
with open(os.path.join(script_dir, universities_rel_path)) as o:
    for line in o:
        universities.append(line.strip())


def location_check(form, field):
    if field.data not in cities:
        raise ValidationError('{} is not a valid city.'.format(field.data))


class UserCreation(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fullname = StringField('FullName', validators=[DataRequired()])
    phone = StringField('Phone', validators=[])
    major = StringField('Major', validators=[DataRequired()])
    college = StringField('College', validators=[DataRequired()])

    graduationMonth = IntegerField('Graduation Month', validators=[DataRequired()])
    graduationYear = IntegerField('Graduation Year', validators=[DataRequired()])
    gpa = StringField('GPA', validators=[DataRequired()])
    currentLocation = StringField('CurrentLocation', validators=[DataRequired(), location_check])
    desiredLocation1 = StringField('DesiredLocation1', validators=[DataRequired(), location_check])
    desiredLocation2 = StringField('DesiredLocation2', validators=[DataRequired(), location_check])
    desiredLocation3 = StringField('DesiredLocation3', validators=[DataRequired(), location_check])
    binaryResume = FileField('Resume', validators=[FileRequired(),
                                                   FileAllowed(['pdf', 'docx', 'doc', 'txt'],
                                                               'Only pdf, docx, doc, txt, supported!')])
    submit = SubmitField('Store')


    def validate_email(self, field):
        if bfly.users.models.User.query.filter_by(id=field.data).first():
            raise ValidationError("Email already in use")

    def validate_phone(self, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

    def validate_major(self, field):
        if field.data not in majors:
            raise ValidationError("{} is not a valid major.".format(field.data))

    def validate_college(self, field):
        if field.data not in universities:
            raise ValidationError("{} is not a valid college/university".format(field.data))

    def validate_graduationMonth(self, field):
        if field.data < 0 or field.data > 12:
            raise ValidationError("{} is not a valid month.".format(field.data))

    def validate_graduationYear(self, field):
        if field.data < 2019:
            raise ValidationError("{} is in the past".format(field.data))

        if field.data > 2030:
            raise ValidationError("{} is too far in the future".format(field.data))

    def validate_gpa(self, field):
        if len(field.data) > 3 or '.' not in field.data:
            raise ValidationError("{} is not in the expected format X.Y".format(field.data))

        first_digit, second_digit = field.data.split('.')
        if int(second_digit) < 0 or int(first_digit) < 0 or int(first_digit) > 4:
            raise ValidationError("GPA is out of 4.0")
