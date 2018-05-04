from digest import app, db
from digest.login.user import get_session_user

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name, teacher):
        self.name = name

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

class OrganizationPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', backref="permissions", foreign_keys=[user_id])
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    org = db.relationship('Organization', backref="permissions", foreign_keys=[org_id])
    is_admin = db.Column(db.Boolean)


    def __init__(self, user, org, is_admin):
        self.user_id = user.id
        self.user = user
        self.org_id = org.id
        self.org = org
        self.is_admin = is_admin
        db.session.add(self)
        db.session.commit()

class ClubSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', backref="subscriptions", foreign_keys=[user_id])
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    org = db.relationship('Organization', backref="subscriptions", foreign_keys=[org_id])

    def __init__(self, user, org):
        self.user_id = user.id
        self.user = user
        self.org_id = org.id
        self.org = org
        db.session.add(self)
        db.session.commit()
