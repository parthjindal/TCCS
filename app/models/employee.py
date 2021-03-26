from datetime import datetime
from enum import unique
from app import login
from flask_login.mixins import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Employee(db.Model, UserMixin):
    '''
        Base Class Employee
        @parameters:
            name:string
            branch:string
            email:string
            password_hash:string
    '''
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)                 # name
    branchID = db.Column(db.Integer, db.ForeignKey(
        'office.id'))                                           # many-to-one Employee->Office
    email = db.Column(db.String(120), index=True, unique=True)  # unique mail
    password_hash = db.Column(
        db.String(128))  # hashed password
    role = db.Column(db.String(64))

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
        'polymorphic_on': role
    }

    def set_password(self, password: str = None):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str = None):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Employee: {self.name}, Role: {self.role}>'


class Manager(Employee):
    manager_name = db.Column(db.String(64), index=True)
    headOffice = db.Column(db.Integer, db.ForeignKey('head.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }

    def __repr__(self):
        return f'<Manager: {self.name} email: {self.email}>'
    pass


@login.user_loader
def load_user(id):
    user = Employee.query.get(int(id))
    if user is None:
        user = Manager.query.get(int(id))
    return user
