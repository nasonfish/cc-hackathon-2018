from digest.org import org
from digest.content import Content
from digest.containers import Organization
from digest.util import render_template_or_json
from digest.login.user import get_session_user, login_required
from flask import request, redirect, url_for, flash, send_from_directory, get_flashed_messages, jsonify
from markdown import markdown
from digest import app, db, allowed_file
from werkzeug import secure_filename
import os
import time
import json
from PIL import Image

def render_view(template, org, _content=None, _units=None, _subjects=None, **kwargs):
    if not _content:
        _content = org.content
    return render_template_or_json(template, org=org, content=_content,
                                   units=_units, subjects=_subjects, **kwargs)

@login_required
@org.route("/")
@org.route("/list")
def list():
    return render_template_or_json("list.html", classes=Organization.query)

@login_required
@org.route("/<id>")
def view(id):
    cls = Organization.query.get_or_404(id)
    return render_view("view.html", cls)

def new_content(id, storage, cls=None, **kwargs):
    if not cls:
        cls = Organization.query.get_or_404(id)
    unit = None
    subject = None
    return storage(request.form['title'], request.form['description'], cls, get_session_user(), unit=unit, subject=subject, **kwargs)

@login_required
@org.route("/<id>/submit/text", methods=['POST'])
def new_text_content(id):
    new_content(id, Content, text=request.form['text'])
    return redirect(url_for('.view', id=id))


@login_required
@org.route("/<id>/subscribe")
def subscribe(id):
    org = Organization.query.get_or_404(id)
    org.subscribe(get_session_user())
    return redirect(url_for('.list'))

@login_required
@org.route("/<id>/unsubscribe")
def unsubscribe(id):
    cls = Organization.query.get_or_404(id)
    cls.unsubscribe(get_session_user())
    return redirect(url_for('.list'))

@login_required
@org.route("/<id>/edit/<content_id>")
def edit(id, content_id):
    cls = Organization.query.get_or_404(id)
    content = Organization.query.get_or_404(content_id)
    return render_template_or_json("edit.html", cls=cls, content=content)
