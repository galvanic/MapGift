from flask import Flask
import os

###

app = Flask(__name__)

app.config.update(
    # CSRF_ENABLED = True,
    # SECRET_KEY = csrf_secret_key,
)

### Database stuff

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

from models import db

## bind db, the SQLachemy instance, to the app so that it knows
## which database to use
db.init_app(app)

with app.app_context():
    db.create_all()

###

import mapapp.routes
