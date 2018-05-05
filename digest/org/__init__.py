from flask import Blueprint
org = Blueprint('org', __name__, template_folder='templates', static_folder='static')

import digest.org.views