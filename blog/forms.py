from wtforms import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, \
    BooleanField
from wtforms.fields.html5 import EmailField


def length_check(form, field):
    if len(field.data) == 0:
        raise ValidationError('Fields should not be null')


class AddPostForm(Form):
    title = TextField('Title')
    description = TextAreaField('Description')


class SignUpForm(Form):
    username = TextField('User Name')
    password = PasswordField('Password')
    email = EmailField('Email')
    submit = SubmitField('Sign Up')


class SignInForm(Form):
    email = EmailField('Email')
    password = PasswordField('Password')
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')


class AboutUserForm(Form):
    firstname = TextField('First Name')
    lastname = TextField('Last Name')
    username = TextField('User Name')
    password = PasswordField('Password')
    email = EmailField('Email')
