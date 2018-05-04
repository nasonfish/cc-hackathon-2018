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
    cls_id = db.Column(db.Integer, db.ForeignKey("class.id"))
    cls = db.relationship('Class', backref="content", foreign_keys=[cls_id])
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    uploader = db.relationship('User', backref="content", foreign_keys=[uploader_id])
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    unit = db.relationship('Unit', backref="content", foreign_keys=[unit_id])
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"))
    subject = db.relationship('Subject', backref="content", foreign_keys=[subject_id])

    __mapper_args__ = {
        'polymorphic_on': type
    }

    def __init__(self, title, description, cls, uploader, unit=None, subject=None, pinned=False, timestamp=False):
        self.title = title
        self.description = description
        if not timestamp:
            timestamp = int(time.time())
        self.timestamp = timestamp
        self.cls_id = cls.id
        self.cls = cls
        self.uploader_id = uploader.id
        self.uploader = uploader
        if unit:
            self.unit_id = unit.id
            self.unit = unit
        if subject:
            self.subject_id = subject.id
            self.subject = subject
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

    @classmethod
    def submit(cls, id):
        return url_for("class.new_text_content", id=id)

    @classmethod
    def args(cls):
        return [{"label": {"for": "content-text", "innerHTML": "Text: "}},
                {"textarea": {"name": "text", "id":"content-text"}}]

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

    @classmethod
    def submit(cls, id):
        return url_for("class.new_picture_content", id=id)

    @classmethod
    def args(cls):
        return [{"label": {"for": "content-picture", "innerHTML": "Picture: "}},
                {"input": {"name": "picture", "type": "file", "id": "content-picture"}}]


class LinkStorage(Content):
    id = db.Column(db.Integer, db.ForeignKey("content.id"), primary_key=True)
    link = db.Column(db.String(64))

    def __init__(self, title, description, cls, uploader, unit, subject, link):
        super(LinkStorage, self).__init__(title, description, cls, uploader, unit, subject)
        self.link = link
        db.session.add(self)
        db.session.commit()

    __mapper_args__ = {
        'polymorphic_identity': 'link'
    }

    def get_print(self, show=True, show_cls=False, show_tags=True):
        return render_template("content/content-link.html", content=self, show_cls=show_cls, show_tags=show_tags)

    @classmethod
    def submit(cls, id):
        return url_for("class.new_link_content", id=id)

    @classmethod
    def args(cls):
        return [{"label": {"for": "content-link", "innerHTML": "Link: "}, "input": {"name": "link", "type": "text", "id": "content-link"}}]


class NotecardStorage(Content):
    id = db.Column(db.Integer, db.ForeignKey("content.id"), primary_key=True)

    def __init__(self, title, description, cls, uploader, unit, subject):
        super(NotecardStorage, self).__init__(title, description, cls, uploader, unit, subject)
        db.session.add(self)
        db.session.commit()

    __mapper_args__ = {
        'polymorphic_identity': 'notecard'
    }

    def new_card(self, text, value):
        Notecard(text, value, self)

    def get_print(self, show_cls=False, show_tags=True):
        return render_template("content/content-notecard.html", content=self, show_cls=show_cls, show_tags=show_tags)

    @classmethod
    def submit(cls, id):
        return url_for("class.new_notecard_content", id=id)

    @classmethod
    def args(cls):
        return []

class Notecard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storage_id = db.Column(db.Integer, db.ForeignKey("notecard_storage.id"))
    storage = db.relationship('NotecardStorage', backref="cards", foreign_keys=[storage_id])
    text = db.Column(db.String(255))
    value = db.Column(db.Text)

    def __init__(self, text, value, storage):
        self.text = text
        self.value = value
        self.storage_id = storage.id
        self.storage = storage

        db.session.add(self)
        db.session.commit()

    def update(self, text, value):
        self.text = text
        self.value = value

        db.session.add(self)
        db.session.commit()

class Classification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(32))

    __mapper_args__ = {
        "polymorphic_on": type
    }

    def __init__(self, name):
        self.name = name

    def amount(self):
        return len(self.content)

class Unit(Classification):
    id = db.Column(db.Integer, db.ForeignKey("classification.id"), primary_key=True)
    cls_id = db.Column(db.Integer, db.ForeignKey("class.id"))
    cls = db.relationship('Class', backref="units", foreign_keys=[cls_id])
    archived = db.Column(db.Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_identity": 'unit'
    }

    def __init__(self, name, cls, archived=False):
        super(Unit, self).__init__(name)
        self.cls_id = cls.id
        self.cls = cls
        self.archived = archived

        db.session.add(self)
        db.session.commit()

    def archive(self, archive=True):
        self.archived = archive
        db.session.add(self)
        db.session.commit()

    def link(self):
        return url_for("class.unit", id=self.cls_id, unit_id=self.id)

class Subject(Classification):
    id = db.Column(db.Integer, db.ForeignKey("classification.id"), primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    unit = db.relationship('Unit', backref="subjects", foreign_keys=[unit_id])

    __mapper_args__ = {
        "polymorphic_identity": 'subject'
    }

    def __init__(self, name, unit):
        super(Subject, self).__init__(name)
        self.unit_id = unit.id
        self.unit = unit

        db.session.add(self)
        db.session.commit()

    def link(self):
        return url_for("class.subject", id=self.unit.cls_id, subject_id=self.id)