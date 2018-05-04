from digest import app, db
from flask import render_template, url_for
import time
import json

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    type = db.Column(db.String(16))
    pinned = db.Column(db.Boolean)
    description = db.Column(db.String(255))
    timestamp = db.Column(db.Integer)
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    org = db.relationship('Organization', backref="content", foreign_keys=[org_id])
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    uploader = db.relationship('User', backref="content", foreign_keys=[uploader_id])

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __init__(self, title, description, org, uploader, pinned=False, timestamp=False):
        self.title = title
        self.description = description
        if not timestamp:
            timestamp = int(time.time())
        self.timestamp = timestamp
        self.org_id = org.id
        self.org = org
        self.uploader_id = uploader.id
        self.uploader = uploader
        self.pinned = pinned
        db.session.add(self)
        db.session.commit()

    def get_print(self, show_cls=False, show_tags=True):
        return render_template("content/content.html", content=self, show_cls=show_cls, show_tags=show_tags)

    @classmethod
    def submit(cls, id):
        pass

    @classmethod
    def args(cls):
        pass  # list(html tag name => (attr => val, attr2 => val...), ...)

    @classmethod
    def json_args(cls):
        return json.dumps(cls.args())

class TextStorage(Content):
    id = db.Column(db.Integer, db.ForeignKey("content.id"), primary_key=True)
    text = db.Column(db.Text())

    def __init__(self, title, description, cls, uploader, unit, subject, text):
        super(TextStorage, self).__init__(title, description, cls, uploader, unit, subject)
        self.text = text
        db.session.add(self)
        db.session.commit()

    __mapper_args__ = {
        'polymorphic_identity': 'text'
    }


    def get_print(self, show_cls=False, show_tags=True):
        return render_template("content/content-text.html", content=self, show_cls=show_cls, show_tags=show_tags)

class PictureStorage(Content):
    id = db.Column(db.Integer, db.ForeignKey("content.id"), primary_key=True)
    filename = db.Column(db.String(255))

    def __init__(self, title, description, cls, uploader, unit, subject, filename, timestamp=False):
        super(PictureStorage, self).__init__(title, description, cls, uploader, unit, subject, timestamp=timestamp)
        self.filename = filename
        db.session.add(self)
        db.session.commit()

    __mapper_args__ = {
        'polymorphic_identity': 'picture'
    }

    def get_print(self, show_cls=False, show_tags=True):
        return render_template("content/content-picture.html", content=self, show_cls=show_cls, show_tags=show_tags)
