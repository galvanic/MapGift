from flask import Flask


app = Flask(__name__)


app.config.update(
    # CSRF_ENABLED = True,
    # SECRET_KEY = csrf_secret_key,
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


from models import db

## bind db, the SQLachemy instance, to the app so that it knows
## which database to use
db.init_app(app)

with app.app_context():
    db.create_all()


import mapapp.routes