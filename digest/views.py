from digest import app
from digest.login.user import get_session_user
from digest.util import render_template_or_json
from digest.content import Content
from flask import redirect, url_for

@app.route('/')
def index():
    if get_session_user():
        return render_template_or_json("index.html")
    return render_template_or_json("welcome.html")