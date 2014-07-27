from flask import Flask


app = Flask(__name__)

with open('keys.txt', 'r') as ifile:
    csrf_secret_key = ifile.read().strip()


app.config.update(
    CSRF_ENABLED = True,
    SECRET_KEY = csrf_secret_key,
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

from models import db
## bind db, the SQLachemy instance, to the app so that it knows which database to use
db.init_app(app)

import mapapp.routes