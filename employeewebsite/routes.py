
from flask import render_template, url_for, flash, redirect, request, abort
from employeewebsite import app, db, bcrypt
from employeewebsite.forms import (RegistrationForm, LoginForm, EmployeeDataForm)
from employeewebsite.models import User, Employee
from flask_login import login_user, current_user, logout_user, login_required

"""This is the login required home route, only authenticated users can access, then the user can view of the homepage
displayed employees based on date posted, employees are ordered by the latest at the top of page 
(The Home Link in the Navigation Bar or The Sign In Button(if valid) on Login Page)"""


@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    employees = Employee.query.order_by(Employee.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', employees=employees)


"""This is the register route, this is a form that takes email and password as input and 
encrypted password is added to database, if the email is taken then cannot be re-added, after valid email and password
 is submitted the routed to login page (The Register Link on Login Page)"""


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


"""This is the login route, validates that input from form is a valid user email and password in database, 
if so then routed to home route (The Sign In Link(if valid) on Register Page or The initial main route)"""


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


"""This logs the user out of the authenticated user, routes to home, then to login. [User will have to login to
 authenticate in order to access the homepage (The Logout Link on Navigation Bar)"""


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


"""This is the login required route that enables users to input data into form which adds employee data into database, 
which then the employee date posted, name and email gets displayed on homepage (The Add Button on Home Page)"""


@app.route("/employee/add", methods=['GET', 'POST'])
@login_required
def add_employee_data():
    form = EmployeeDataForm()
    if request.method == 'POST':
        new_employee = Employee(
            email=request.form['email'],
            name=request.form['name'],
            address=request.form['address'],
            city=request.form['city'],
            state=request.form['state'],
            zip=request.form['zip'],
            phone=request.form['phone'])
        db.session.add(new_employee)
        db.session.commit()
        flash('New Employee Data has been Added', 'success')
        return redirect(url_for('home'))
    return render_template('update_employee_data.html', title='Add Employee Information',
                           form=form, legend='Add Employee')


"""This is a login required route that enables users to view employee data, users can access this data by clicking  
employee email link on homepage, the employee data is then pulled based upon employee_id of employee
the employee_id then linked to all the employee object data (The Employee Email Link on Homepage)"""


@app.route("/employee/<int:employee_id>")
@login_required
def display_employee_data(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('employee_data.html', title='Employee Information', employee=employee)


"""This is a login required route that allows users to edit employee data, this function can be access by clicking 
employee name link, and by clicking update from the display of employee data page. The data is pulled by 
employee_id of Employee object. The submitted data from the form that is inputted by the user, then 
updates the employee data in database these updated can be seen after flash ("Your Employee data has been updated") on 
the display of employee data page (The Update Button on Display Page or The Employee Name Link on Homepage)"""


@app.route("/employee/<int:employee_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_employee_data(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeDataForm()
    if request.method == 'POST':
        employee.email = form.email.data
        employee.name = form.name.data
        employee.address = form.address.data
        employee.city = form.city.data
        employee.state = form.state.data
        employee.zip = form.zip.data
        employee.phone = form.phone.data
        db.session.commit()
        flash('Your employee data has been updated!', 'success')
        return redirect(url_for('display_employee_data', employee_id=employee.id))
    elif request.method == 'GET':
        form.email.data = employee.email
        form.name.data = employee.name
        form.address.data = employee.address
        form.city.data = employee.city
        form.state.data = employee.state
        form.zip.data = employee.zip
        form.phone.data = employee.phone
    return render_template('update_employee_data.html', title='Update Employee Information',
                           form=form, legend='Update Employee')


"""This is a login required route that allows user to delete employee object from database, the function is accessable 
by clicking the employee email link of homepage, then routes to display of employee data, the delete button on the 
display employee data page will remove employee from database(The Delete Button on Display Page)"""


@app.route("/employee/<int:employee_id>/delete", methods=['POST'])
@login_required
def delete_employee_data(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Your Employee has been deleted!', 'success')
    return redirect(url_for('home'))
