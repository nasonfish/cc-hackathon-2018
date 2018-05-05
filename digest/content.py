from digest import app, db
from flask import render_template, url_for
import time
import json

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    type = db.Column(db.String(16))
    pinned = db.Column(db.Boolean)
    timestamp = db.Column(db.Integer)
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    org = db.relationship('Organization', backref="content", foreign_keys=[org_id])
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    uploader = db.relationship('User', backref="content", foreign_keys=[uploader_id])
    text = db.Column(db.Text())

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __init__(self, title, org, uploader, text, pinned=False, timestamp=False):
        self.title = title
        if not timestamp:
            timestamp = int(time.time())
        self.timestamp = timestamp
        self.org_id = org.id
        self.org = org
        self.uploader_id = uploader.id
        self.uploader = uploader
        self.pinned = pinned
        self.text = text
        db.session.add(self)
        db.session.commit()

    def get_print(self, show_cls=False, show_tags=True):
        return render_template("content/content.html", content=self, show_cls=show_cls, show_tags=show_tags)

    @classmethod
    def submit(cls, id):
        pass

    @classmethod
    def json_args(cls):
        return json.dumps(cls.args())


    def get_print(self, show_cls=False, show_tags=True):
        return render_template("content/content-text.html", content=self, show_cls=show_cls, show_tags=show_tags)
