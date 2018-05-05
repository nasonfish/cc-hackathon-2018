from digest import app
from digest.login.user import get_session_user, admin_required
from digest.util import render_template_or_json
from digest.content import Content
from digest.containers import Organization, OrganizationSubscription
from flask import redirect, url_for

@app.route('/')
def index():
    user = get_session_user()
    if user:
        content = Content.query.join(Organization).join(OrganizationSubscription).filter \
            (OrganizationSubscription.user_id == user.id).order_by(Content.timestamp.desc()).limit(20).all()
        return render_template_or_json("index.html", content=content)
    return render_template_or_json("welcome.html")

@app.route('/admin')
@admin_required
def admin():
    return render_template_or_json("admin.html")