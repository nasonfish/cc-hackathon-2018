#!/usr/bin/env python3.4
from digest import app

from digest.scaffolding import scaffolding
from digest.login import login
from digest.account import account
from digest.org import org

# register the branding module as a blueprint
app.register_blueprint(scaffolding, url_prefix='/branding')
app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(org, url_prefix="/org")
