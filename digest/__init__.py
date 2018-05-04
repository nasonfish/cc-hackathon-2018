from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.sendmail import Mail
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('digest.conf')
db = SQLAlchemy(app)
mail = Mail(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

import school.filters
import school.user
import school.login.session
import school.containers
import school.content
import school.views


app.add_url_rule('/static/<path:filename>',
                 endpoint='static',
                 view_func=app.send_static_file)