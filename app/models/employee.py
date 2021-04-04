from app import login, db
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class Employee(db.Model, UserMixin):
    '''
    '''
    ####################################### ORM ##############################################
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    branchID = db.Column(db.Integer, db.ForeignKey('office.id'), index=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))

    role = db.Column(db.String(64))

    __mapper_args__ = {

        'polymorphic_identity': 'employee',
        'polymorphic_on': role
    }

    ##########################################################################################

    def __init__(self, **kw):
        '''
        '''
        super().__init__(**kw)

    def set_password(self, password: str = None):
        '''
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str = None):
        '''
        '''
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        '''
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        '''
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Employee.query.get(user_id)

    def __repr__(self):
        return f'<Employee: {self.name}, Role: {self.role}>'


class Manager(Employee):
    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }

    def change_rate(self, rate):
        pass

    def __repr__(self):
        return f'<Employee: {self.name} Role: {self.role}>'


@login.user_loader
def load_user(id):
    user = Employee.query.get(int(id))
    return user
