#!/usr/bin/env python
# coding: utf-8

import os
from flask import  (Flask,
                    render_template,
                    send_from_directory,
                    request)
from flask.ext.sqlalchemy import SQLAlchemy


###
### initialization
###


with open('keys.txt', 'r') as ifile:
    csrf_secret_key = ifile.read().strip()


app = Flask(__name__)
app.config.update(
    DEBUG = True,
    CSRF_ENABLED = True,
    SECRET_KEY = csrf_secret_key,
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


###
### helper functions
###


import mapgift


def update_map_list():
    """Gets all map objects from db and the next map id"""
    # counts maps
    return [], 1


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


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html',
            providers   = mapgift.PROVIDERS,
            next_map_id = update_map_list()[1])


@app.route('/archive')
def archive():

    return render_template('archive.html',
            map_list = update_map_list()[0])


@app.route('/assemble', methods=['POST'])
def assemble():

    ## get info from the form in the index page
    map_id = int(request.form['map_id'])
    design = request.form['design']
    zoom   = int(request.form['zoom2'])
    coord  = request.form['coord']
    coord  = tuple(map(float, coord.split(', ')))
    if request.files:
        # need to check this file [security] TODO FIXME
        kmlfile = request.files['placemarks'].read()
    else:
        kmlfile = ''

    ## make the map image (PIL.Image object returned here)
    m_img = mapgift.main(   map_provider = design,
                            area         = coord,
                            zoom         = zoom,
                            by_centre    = True,
                            kmlfile      = kmlfile)
    
    from code import interact; interact(local=dict( globals(), **locals() ))

    ## send image off to be stored in S3 through boto
    

    ## save map information as a map object in db


    return render_template('detail.html')


@app.route('/detail/<int:map_id>')
def detail(map_id):

    return render_template('detail.html',
            map = map_id)


###
### launch app
###


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)







