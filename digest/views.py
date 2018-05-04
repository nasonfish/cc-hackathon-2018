from school import app
from school.login.user import get_session_user
from school.util import render_template_or_json
from school.content import Content
from school.containers import Class, UserSubscription
from flask import redirect, url_for

@app.route('/')
def index():
    if get_session_user():
        content = Content.query.join(Class).join(UserSubscription).filter\
            (UserSubscription.user_id == get_session_user().id).order_by(Content.timestamp.desc()).limit(20).all()
        return render_template_or_json("index.html", content=content)
    return render_template_or_json("welcome.html")