import base64
import random
import os
import hashlib
import string
import codecs
from functools import wraps

from digest import db
from digest.login.pbkdf2 import pbkdf2_hex
from flask import session, request, redirect, url_for, abort


class UserSkeleton():
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(255))
    salt = db.Column(db.String(32))
    enabled = db.Column(db.Boolean, default=1)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.assign_password(password)

    def _get_pbkdf2_hash(self, password):
        return pbkdf2_hex(password, self.salt, 1000, 64, hashlib.sha512)

    def validate_password(self, password):
        if self._get_pbkdf2_hash(password) == self.password:
            return True
        return False

    def assign_password(self, new_password):
        self.salt = codecs.encode(os.urandom(16), 'hex')
        self.password = self._get_pbkdf2_hash(new_password)
        db.session.add(self)
        db.session.commit()

    def get_session(self):
        if session.has_key('session_id'):
            sess = Session.query.filter_by(id=session['session_id']).first()
            if not sess:
                return None
            if sess.user is not self:
                return None
            return sess

    def set_pwreset_key(self):
        self.pwreset_key = ''.join([random.choice(string.letters + string.digits) for i in xrange(120)])

        db.session.add(self)
        db.session.commit()

"""
Copyright (c) 2012, 2013, 2014 Centarra Networks, Inc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice, this permission notice and all necessary source code
to recompile the software are included or otherwise available in all
distributions.

This software is provided 'as is' and without any warranty, express or
implied.  In no event shall the authors be liable for any damages arising
from the use of this software.
"""



class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='sessions', foreign_keys=[user_id])

    host = db.Column(db.String(255))
    challenge = db.Column(db.String(255))

    def __init__(self, user):
        self.user_id = user.id
        self.user = user

        self.host = request.remote_addr
        self.challenge = str(base64.b64encode(str(random.getrandbits(256)).encode('ascii')))

        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Session: {0} from {1}>'.format(self.id, self.host)

    def validate(self, challenge):
        return (self.challenge == challenge)

def get_session():
    if 'session_id' in session:
        sess = Session.query.filter_by(id=session['session_id']).first()
        if not sess:
            return None
        if not sess.validate(session['session_challenge']):
            return None
        return sess
    if is_api_session() and get_session_user():
        user = get_session_user()
        sess = Session.query.filter_by(user_id=user.id).filter_by(challenge=user.api_key).first()
        if not sess:
            sess = Session(user)
            sess.challenge = user.api_key
            db.session.add(sess)
            db.session.commit()
        return sess
    return None

def is_api_session():
    return True if request.authorization else False

def get_session_user():
#    if request.authorization:
#        auth = request.authorization
#
#        user = User.query.filter_by(username=auth.username).first()
#        if not user:
#            return None
#        if user.validate_password(auth.password) != True and auth.password != user.api_key:
#            return None
#        return user

    sess = get_session()
    if sess:
        return sess.user

    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        u = get_session_user()
        if not u:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    f.requires_permission = True
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_session_user()
        if user is None:
            return redirect(url_for('login'))
        if not user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function