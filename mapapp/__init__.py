from flask import Flask
import os

###

app = Flask(__name__)

### Database stuff

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
try:
	app.config['DEBUG'] = os.environ.get('HEROKU_DEBUG_STATUS')
except:
	app.config['DEBUG'] = False

from models import db

## bind db, the SQLachemy instance, to the app so that it knows
## which database to use
db.init_app(app)

with app.app_context():
    db.create_all()

###

import mapapp.routes
