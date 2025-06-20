from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User, Employee, IssueReport, Location

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username')
    
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address')
    
class AddEmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_hire = DateField('Hire Date', validators=[DataRequired()])
    location = SelectField('Location', choices=[], validators=[])
    submit = SubmitField('Add Employee')
    
    def __init__(self, *args, **kwargs):
        super(AddEmployeeForm, self).__init__(*args, **kwargs)
        self.location.choices = [(loc.id, loc.location) for loc in Location.query.all()]

class ReportIssueForm(FlaskForm):
    issue = TextAreaField('Work Violation', validators=[DataRequired()], render_kw={'style':'resize: none;'})
    reason = TextAreaField('Violation Reason', validators=[DataRequired()])
    date_of = DateField('Date of Issue', validators=[DataRequired()])
    submit = SubmitField('Record')

class ResetPass(FlaskForm):
    old_pass = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat New Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Change Password')