from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

import bfly.users.models


class UserCreation(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fullname = StringField('FullName', validators=[DataRequired()])
    major1 = StringField('First Major', validators=[DataRequired()])
    major2 = StringField('Second Major', validators=[])
    major3 = StringField('Third Major', validators=[])
    college = StringField('College', validators=[DataRequired()])
    graduationMonth = IntegerField('Graduation Month')
    graduationYear = IntegerField('Graduation Year')
    submit = SubmitField('Store')

    def validate_email(self, field):
        if bfly.users.models.User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already in use")
