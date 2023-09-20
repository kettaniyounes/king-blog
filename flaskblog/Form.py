from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flaskblog.modules import User
from flask_login import current_user


class SingUPForm(FlaskForm):

    username = StringField('User Name', validators=[DataRequired(), Length(max=20, min=5)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirme password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already exist! please chouse another one!')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This username is already exist! please chouse another one!')

class LogInForm(FlaskForm):

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Rememer me?')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):

    username = StringField('User Name', validators=[DataRequired(), Length(max=20, min=5)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    picture_profile = FileField('Update Profile', validators=[FileAllowed(['jpg', 'png'], 'Only JPG and PNG files are allowed.')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already exist! please chouse another one!')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already exist! please chouse another one!')
            

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')