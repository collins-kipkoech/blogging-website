from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired])
    confirm_password = PasswordField('Confirm_Password',validators=[DataRequired, EqualTo('password')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    
    password = PasswordField('Password',validators=[DataRequired])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

