import sqlalchemy as sa
from datetime import date
from flask import render_template,flash,redirect, url_for, request,abort
from app import app,db
from app.models import User, Employee, IssueReport, Location
from app.forms import LoginForm, RegistrationForm, ReportIssueForm, AddEmployeeForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from functools import wraps

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_functions(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role_name):
                return redirect(url_for('login'))
            return f(*args,**kwargs)
        return decorated_functions
    return decorator


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home Page')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
@role_required('admin')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, first_name=form.f_name.data, last_name=form.l_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User now registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register User', form=form)

@app.route('/late_reporter/<emp_id>', methods=['GET','POST'])
@role_required('admin')
def record_late(emp_id):
    form = ReportIssueForm()
    employee = db.session.scalar(sa.select(Employee).where(Employee.id == emp_id))
    if employee is None:
        return redirect(url_for('employee_listing'))
    if form.validate_on_submit():
        writeup=IssueReport(emp_id=emp_id, user_id=current_user.id, issue=form.issue.data, reason=form.reason.data, date_of=form.date_of.data)
        db.session.add(writeup)
        db.session.commit()
        return redirect(url_for('employee_listing'))
    return render_template('recordlate.html', title='Late Record', form=form, employee=employee)

@app.route('/employees')
@role_required('admin')
def employee_listing():
    employees = Employee.query.all()
    locations = db.session.scalars(sa.select(Location)).all()
    print(locations)
    for e in employees:
        print(e)
    return render_template('employeelisting.html', title='Employees', employees=employees, locations=locations)

@app.route('/addemployee', methods=['GET','POST'])
@role_required('admin')
def add_employee():
    form = AddEmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(first_name=form.first_name.data, last_name=form.last_name.data,date_of_hire=form.date_of_hire.data, location_id=form.location.data)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('employee_listing'))
    return render_template('addemployee.html', title='Add Employee', form=form)

@app.route('/terminate_employee/<emp_id>', methods=['GET','POST'])
@role_required('admin')
def term_employee(emp_id):
    term_employee = Employee.query.get(emp_id)
    term_employee.date_of_term = date.today()
    term_employee.emp_active = False
    db.session.commit()
    return redirect(url_for('employee_listing'))

@app.route('/worker_record/<emp_id>')
@role_required('admin')
def worker_record(emp_id):
    employee = Employee.query.get(emp_id)
    reports = IssueReport.query.where(IssueReport.emp_id == emp_id).all()
    users = User.query.all()
    return render_template('record.html', title=f"{employee.first_name}", employee=employee, reports=reports, users=users)