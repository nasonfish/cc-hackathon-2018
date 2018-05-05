#!/usr/bin/env python
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

import blinker
import time

from digest import app, db
from digest.login.user import Session, get_session_user, login_required, User
from flask import session, redirect, url_for, escape, request, jsonify, escape, render_template

login_signal = blinker.Signal('A signal sent when the user logs in')
logout_signal = blinker.Signal('A signal sent when the user logs out')
authfail_signal = blinker.Signal('A signal sent when the user fails authentication')

@login_signal.connect_via(app)
def handle_session_login(*args, **kwargs):
    user = kwargs.pop('user', None)
    sess = Session(user)
    session['session_id'] = sess.id
    session['session_challenge'] = sess.challenge
    user.signin_time = time.time()
    db.session.add(user)
    db.session.commit()

@logout_signal.connect_via(app)
def handle_session_logout(*args, **kwargs):
    sess = Session.query.filter_by(id=session['session_id']).first()

    if sess:
        db.session.delete(sess)
        db.session.commit()

    session.pop('session_id')
    session.pop('session_challenge')

def validate_login(username, password):
    u = User.query.filter_by(username=username).first()
    if u is None or not u.enabled:
        authfail_signal.send(app, user=u, reason='Invalid username')
        return False
    if u.validate_password(password) is False:
        authfail_signal.send(app, user=u, reason='Invalid password')
        return False
    # Password validation was successful, fire the login event.
    login_signal.send(app, user=u)
    return True

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = validate_login(request.form['username'], request.form['password'])
        if user is not False:
            return redirect(url_for('index'))
        else:
            session.pop('session_id', None)
            session.pop('session_challenge', None)
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    _user = get_session_user()
    if _user is not None:
        logout_signal.send(app, user=_user)

    return redirect(url_for('index'))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        redir_target = request.form.get('outmodule', 'index')

        try:
            username = request.form['username'].strip().rstrip()
            password = request.form['password'].strip().rstrip()
            email = request.form['email'].strip().rstrip()
            if len(username) == 0:
                return render_template('create.html', error='No username provided')
            if escape(username) != username or ' ' in username:
                return render_template('create.html', error='Username contains invalid characters')
            if len(password) == 0:
                return render_template('create.html', error='No password provided')
            if len(email) == 0:
                return render_template('create.html', error='No email provided')
            if escape(email) != email or '@' not in email:
                return render_template('create.html', error='E-mail address is malformed')
            user = User(username, email, password)
        except:
            return render_template('create.html', error='Username is already taken')
            
        if user is not None:
            sess = Session(user)
            session['session_id'] = sess.id
            session['session_challenge'] = sess.challenge
            return redirect(url_for(redir_target))

    return render_template('create.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset_ui():
    if request.method == 'POST':
        username = request.form.get('username', '').strip().rstrip()
        email = request.form.get('email', '').strip().rstrip()
        from digest.login.user import User
        user = User.query.filter_by(username=username).filter_by(email=email).first()

        if not user:
            return render_template('lost-password.html', error='The information provided does not match any account on file')

        user.set_pwreset_key()
        user.send_email('Please confirm your password reset request', 'email/lost-password-confirm.txt')

        return render_template('lost-password.html', error='A confirmation message has been sent to the e-mail address on file')

    return render_template('lost-password.html')

@app.route('/reset-confirm/<pwreset_key>', methods=['GET', 'POST'])
def reset_confirm(pwreset_key):
    user = User.query.filter_by(pwreset_key=pwreset_key).first_or_404()

    if request.method == 'POST':
        password = request.form['password'].strip().rstrip()
        user.assign_password(password)
        user.set_pwreset_key()

        return redirect(url_for('login'))

    return render_template('lost-password-confirm.html', user=user)

@app.context_processor
def user_information_from_session():
    """A decorated function to give the templates a user object if we're logged in."""
    _user = get_session_user()
    if _user is not None:
        return dict(user=_user)

    return dict()
