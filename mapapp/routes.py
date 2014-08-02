import os
import datetime

from mapapp import app
from flask  import  (render_template,
                    send_from_directory,
                    request,
                    redirect,
                    url_for)

from models import db
from models import Map, KMLfile


###
### helper functions
###


from PIL import Image
import mapgift
import cStringIO

def update_map_list():
    """Gets all map objects from db and the next map id"""
    ## get maps
    map_list = db.session.query(Map).order_by(Map.pub_date.desc()).all()
    next_map_id = len(map_list)+1
    return map_list, next_map_id


import boto
from boto.s3.key        import Key
from boto.s3.connection import S3Connection

AWS_ACCESS_KEY  = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY  = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

def send_image_s3(img_file, image_filename):
    """"""
    conn   = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = conn.get_bucket(AWS_BUCKET_NAME)
    k      = Key(bucket)
    k.key  = image_filename
    k.set_contents_from_string(img_file.getvalue())
    k.make_public()
    return


###
### controllers: other
###


@app.route('/style.css')
def css():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'css/style.css')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


###
### controllers: main pages
###


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html',
            providers   = mapgift.PROVIDERS,
            next_map_id = update_map_list()[1]
            )


@app.route('/archive')
def archive():

    return render_template('archive.html',
            map_list    = update_map_list()[0],
            bucket_name = AWS_BUCKET_NAME
            )


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
    
    ## send image off to be stored in S3 through boto
    m_img_file = cStringIO.StringIO()
    m_img.save(m_img_file, 'PNG')
    map_name = 'map%s.png' % str(map_id)
    send_image_s3(m_img_file, map_name)

    ## make a thumbnail annd send it to AWS
    m_thumbnail = m_img.resize(map(lambda n: n/4, m_img.size),
                               Image.ANTIALIAS)
    m_thumbnail_file = cStringIO.StringIO()
    m_thumbnail.save(m_thumbnail_file, 'PNG')
    thumb_name = 'thumbnail%s.png' % str(map_id)
    send_image_s3(m_thumbnail_file, thumb_name)

    del m_img, m_img_file, m_thumbnail, m_thumbnail_file

    ## save map information as a map object in db
    where = ', '.join(map(str, coord))
    m = Map(
        area_name    = where, # TODO should reverse geolocalise this to get an actual name
        zoom         = zoom,
        map_provider = design,
        pub_date     = datetime.datetime.now()
    )
    db.session.add(m)
    db.session.commit()

    return redirect(url_for('detail', map_id = map_id))


@app.route('/detail/<int:map_id>')
def detail(map_id):

    ## get map object from the database
    m = db.session.query(Map).filter(Map.id == map_id).one()
    return render_template('detail.html',
            map         = m,
            bucket_name = AWS_BUCKET_NAME)














