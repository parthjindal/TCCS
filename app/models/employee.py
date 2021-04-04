from app import login, db
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class Employee(db.Model, UserMixin):
    """
        A class to represent an employee
        ....

        Attributes
        ----------
        name: string
            name of the employee

        email: string
            the registered email id of the employee

        branchID: int
            id of the office where the employee is working

        password_hash: string
            hash of the login password of the employee

        Member Functions
        ----------------
        set_password(password: str):
            the function to reset the login password of the employee
        
        check_password(password: str): bool
            the function to check if the given password is equal to login password of the employee
        
        get_reset_token(expire_sec: int): str
            the function to generate a resent token whenever the employee tries to reset the password
        
        verify_reset_token(token: str): int
            verifies the reset token and returns the id of the employee

        __repr__(): str
            returns the string representation of an object of the class 

    """
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
            The constructor of the Employee class
            ...

            Parameters:
                name: string
                    name of the employee
                email: string
                    the registered email id of the employee
                branchID: int
                    id of the office where the employee is working
        '''
        super().__init__(**kw)

    def set_password(self, password: str = None):
        '''
            The function to set the login password of the employee
            ....

            Parameters:
                password: str
                    the new login password of the user
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str = None):
        '''
            The function to check if the hash value of the login password of the employee and 
                        the given password are same
            ...
            
            Parameters:
                password: string
                    the string with which the password of the employee has to be compared
            Returns:
                bool
        '''
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        '''
            The function to generate a reset token when the employee wishes to reset the password
            ...

            Parameters:
                expires_sec: int
                    time duration for which the token will be valid
            Returns:
                str
        '''
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        '''
            The function to verify the reset token and return the id of the employee if 
                    the verification is successful
            ....
            
            Parameters:
                token: string
                    the token to be verified
            Returns:
                user_id: int
        '''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Employee.query.get(user_id)

    def __repr__(self):
        """
            The function to get the string representation of the employee
            ....

            Returns:
                str
        """
        return f'<Employee: {self.name}, Role: {self.role}>'


class Manager(Employee):
    '''
        A class derived from Employee class to represent a manager 
        ....

        Attributes
        ----------
        Same as that of the Employee class

        Member Functions
        ----------------
        All the member functions of the Employee class are present in the Manager class. 
        Aditionally, there are some more member functions in the Manager class

        change_rate(rate: int)
            the function to change the rate of the transportation cost

        __repr__(): str
            returns the string representation of an object of the class 

    '''
    __mapper_args__ = {
        'polymorphic_identity': 'manager'
    }

    def change_rate(self, rate):
        '''
            The function to change the rate of the transporation cost
            ....

            Parameters:
                rate: int
                    the new rate
        '''
        pass

    def __repr__(self):
        """
            The function to get the string representation of the manager
            ....

            Returns:
                str
        """
        return f'<Employee: {self.name} Role: {self.role}>'


@login.user_loader
def load_user(id):
    '''
        function to return the employee with the given id
        ....

        Pararmeters:
            id: int
                the id of the employee to be returned
        
        Returns:
            user: Employee
    '''
    user = Employee.query.get(int(id))
    return user
