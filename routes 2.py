
from flask import render_template, url_for, flash, redirect, request, abort
from employeewebsite import app, db, bcrypt
from employeewebsite.forms import (RegistrationForm, LoginForm, EmployeeDataForm)
from employeewebsite.models import User, Employee
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    employees = Employee.query.order_by(Employee.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', employees=employees)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/employee/add", methods=['GET', 'POST'])
@login_required
def add_employee_data():
    form = EmployeeDataForm()
    if form.request.method == 'POST':
        new_employee = Employee(
            email=request.form['username'],
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
    return render_template('update_employee_data.html', title='Add New Employee',
                           form=form, legend='Add Employee')


@app.route("/employee/<int:employee_id>")
@login_required
def display_employee_data(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('employee_data.html', title=employee.name, employee=employee)


@app.route("/employee/<int:employee_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_employee_data(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeDataForm()
    if form.validate_on_submit():
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


@app.route("/employee/<int:employee_id>/delete", methods=['POST'])
@login_required
def delete_employee_data(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Your Employee has been deleted!', 'success')
    return redirect(url_for('home'))