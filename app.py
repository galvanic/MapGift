import os
from flask import Flask, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy


###
### initialization
###


app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


###
### helper functions
###


import mapgift


###
### controllers: other
###


@app.route('/style.css')
def css():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'css/style.css')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


###
### controllers: main pages
###


@app.route("/")
def index():

    return render_template('index.html',
    		providers   = mapgift.PROVIDERS,
    		next_map_id = 1)


@app.route("/archive")
def archive():

	return render_template('archive.html')


@app.route("/assemble")
def assemble(map_id):

	return render_template('assemble.html')


@app.route("/detail/<map_id>")
def detail(map_id):

	return render_template('detail.html',
            map = map_id)


###
### launch app
###


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)







