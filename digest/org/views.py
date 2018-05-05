from digest.org import org
from digest.content import Content
from digest.containers import Organization, OrganizationPermission
from digest.util import render_template_or_json
from digest.login.user import get_session_user, login_required, admin_required
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
    return render_template_or_json("list.html", orgs=Organization.query)

@login_required
@org.route("/<id>")
def view(id):
    org = Organization.query.get_or_404(id)
    return render_view("view.html", org=org)

@login_required
@org.route("/<id>/submit", methods=['POST'])
def submit(id):
    org = Organization.query.get_or_404(id)
    Content(request.form['title'], org, get_session_user(), request.form['text'])
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

@admin_required
@org.route("/create", methods=['POST'])
def create():
    org = Organization(request.form['name'])
    OrganizationPermission(get_session_user(), org, is_admin=True)
    return redirect(url_for('.view', id=org.id))