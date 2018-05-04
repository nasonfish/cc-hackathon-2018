from digest import app, db
from digest.login.user import get_session_user

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    teacher = db.relationship('Teacher', backref="classes", foreign_keys=[teacher_id])

    def __init__(self, name, teacher):
        self.name = name
        self.teacher_id = teacher.id
        self.teacher = teacher

        db.session.add(self)
        db.session.commit()

    def subscribe(self, user):
        UserSubscription(user, self)

    def unsubscribe(self, user):
        UserSubscription.query.filter_by(cls_id=self.id, user_id=user.id).delete()
        db.session.commit()

    def is_subscribed(self, user=False):
        if not user:
            user = get_session_user()
        return UserSubscription.query.filter_by(cls_id=self.id, user_id=user.id).first() is not None

class UserSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    user = db.relationship('Student', backref="subscriptions", foreign_keys=[user_id])
    cls_id = db.Column(db.Integer, db.ForeignKey("class.id"))
    cls = db.relationship('Class', backref="subscriptions", foreign_keys=[cls_id])

    def __init__(self, user, cls):
        self.user_id = user.id
        self.user = user
        self.cls_id = cls.id
        self.cls = cls
        db.session.add(self)
        db.session.commit()
