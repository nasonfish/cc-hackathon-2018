
from digest import db
from digest.login.user import UserSkeleton
# comment boxes

class User(UserSkeleton, db.Model):
    __tablename__ = "user"
    nice_name = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean)
    type = db.Column(db.String(32))

    def __init__(self, username, email, password, nice_name=False, is_admin=False):
        super(User, self).__init__(username, email, password)
        self.nice_name = nice_name or username
        self.is_admin = is_admin
        db.session.add(self)
        db.session.commit()

    def update(self, nice_name):
        self.nice_name = nice_name
        db.session.add(self)
        db.session.commit()

    __mapper_args__ = {
        'polymorphic_on': type
    }


class Teacher(User):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'teacher'
    }

class Student(User):
    __tablename__ = "student"
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'student'
    }