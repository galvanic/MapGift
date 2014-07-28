from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Map(db.Model):

    __tablename__ = 'maps'

    id           = db.Column(db.Integer, primary_key=True)
    area_name    = db.Column(db.String(40))
    zoom         = db.Column(db.Integer)
    map_provider = db.Column(db.String(20))
    pub_date     = db.Column(db.DateTime)

    def __init__(self, area_name, zoom, map_provider, pub_date):
        self.area_name    = area_name
        self.zoom         = zoom
        self.map_provider = map_provider
        self.pub_date     = pub_date

    def __repr__(self):
        return self.area_name



class KMLfile(db.Model):
    
    __tablename__ = 'kmlfiles'

    id            = db.Column(db.Integer, primary_key=True)
    filename      = db.Column(db.Integer, unique=True)
    date_uploaded = db.Column(db.DateTime)

    def __init__(self, filename, date_uploaded):
        self.filename      = filename
        self.date_uploaded = date_uploaded

    def __repr__(self):
        return self.filename







