from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from employeewebsite.models import User, Employee

"""This is the form used to get input from users, this allows them to register which lets them
be able to login to gain access to login required routes, this form is controlled by register route function
which adds the form data into database if it does not already exist"""

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


"""This is the form used to get input from users, this allows them to login which lets them gain access login required
routes. This form data is validated that exist in database by login route function"""

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


"""This is the form used to get input form users, this allows users to edit and add employee data, this form is 
controlled by edit_employee and add_employee route functions. The edit function takes the input from form and updates 
the data of employee that already exist. The add function adds the input data from the form and add the employee data
to database"""


class EmployeeDataForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=35)])
    address = StringField('Address', validators=[DataRequired(), Length(min=10, max=50)])
    city = StringField('City', validators=[DataRequired(), Length(min=5, max=50)])
    state = SelectField('State', choices=[('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
                                           'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
                                           'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH',
                                           'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD',
                                           'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')],
                        validators=[DataRequired(), Length(min=2, max=3)])
    zip = IntegerField('Zip Code', validators=[DataRequired(), Length(min=5, max=9)])
    phone = IntegerField('Phone Number', validators=[DataRequired(), Length(min=10, max=12)])
    submit = SubmitField('Save')

    def validate_name(self, name):
        employee = Employee.query.filter_by(name=name.data).first()
        if employee is not None:
            raise ValidationError('This Employee already Exist')

    def validate_email(self, email):
        employee = Employee.query.filter_by(email=email.data).first()
        if employee is not None:
            raise ValidationError('That Employee email is taken. Please choose a different one.')

