from digest.account import account
from digest.login.user import login_required, get_session_user
from digest.util import render_template_or_json
from flask import request, flash

@account.route('/', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        user = get_session_user()
        user.update(request.form['nice_name'])
        flash("Successfully updated user settings.")
    return render_template_or_json("account/account.html")
