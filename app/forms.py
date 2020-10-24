from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField,\
    SelectField, TextAreaField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_pagedown.fields import PageDownField

from app.models import User
from app import images


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))
#
#
#
# from flask_wtf import FlaskForm
# from wtforms import StringField, SelectField, FileField, SubmitField, DateField, RadioField
# from wtforms.validators import DataRequired, Email
# from flask_pagedown.fields import PageDownField
# from flask import request
# from flask_babel import _, lazy_gettext as _l


class CreateTicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    content = PageDownField('Content', validators=[DataRequired()])
    file = FileField('Attach File', validators=[FileAllowed(images, ' Images only')])
    department = SelectField('Queue', choices=[('Billing Queries', '[Billing Queries]'), ('Product Issues', '[Product Issues]')])
    priority = SelectField('Priority', choices=[('1', '1. Critical'), ('2', '2. High'), ('3', '3. Normal'), ('4', '4. Low'), ('5', '5. Very Low')])
    # due_date = DateField('Due Date')
    email = StringField('Email', validators=[DataRequired(), Email()])
    # ids = randint(1000, 9999)
    submit = SubmitField('Send Ticket')


class Status(FlaskForm):
    status = RadioField('Status', choices=[('Open', 'Open'), ('Resolved', 'Resolved'), ('Closed', 'Closed')])
    submit = SubmitField('Update This Ticket')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class PostForm(FlaskForm):
    body = PageDownField('Whats on your mind', validators=[DataRequired()])
    submit = SubmitField('Submit')
#
# class SearchForm(FlaskForm):
#     # choices = [('Email', 'Email'), ('Title', 'Title'), ('content', 'content')]
#     # select = SelectField('Search for ticket:', choices=choices)
#     q = StringField(_l('Search', validators=[DataRequired()]))
#
#     def __init__(self, *args, **kwargs):
#         if 'formdata' not in kwargs:
#             kwargs['formdata'] = request.args
#         if 'csrf_enabled' not in kwargs:
#             kwargs['csrf_enaled'] = False
#         super(SearchForm, self).__init__(*args, **kwargs)
#
#
# # a class for showing statistics
# class Stats(Table):
#     title = LinkCol('Title',  'update', url_kwargs=dict(title='title'), anchor_attrs={'class': 'Stats'},
#                        text_fallback='updatestatus.html')
#     priority = Col('Priority')
#     department = Col('Queue')
#     timestamp = Col('Created')
#     due_date = Col('Due Date')
#     status = Col('Status')
#
#
# class CurrentTicket(object):
#     def __init__(self, title, priority, department, timestamp, due_date, file):
#         self.title = title
#         self.priority = priority
#         self.department = department
#         self.timestamp = timestamp
#         self.due_date = due_date
#         self.file = file
#
#
# # for updating status
#
#
