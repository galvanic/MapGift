from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime
from database import Base


db = SQLAlchemy()


class Map(Base):

    __tablename__ = 'maps'

    id           = Column(Integer, primary_key=True)
    area_name    = Column(String(40))
    zoom         = Column(Integer)
    map_provider = Column(String(20))
    pub_date     = Column(DateTime)

    def __init__(self, area_name, zoom, map_provider, pub_date):
        self.area_name    = area_name
        self.zoom         = zoom
        self.map_provider = map_provider
        self.pub_date     = pub_date

    def __repr__(self):
        return self.area_name



class KMLfile(Base):
    
    __tablename__ = 'kmlfiles'

    id            = Column(Integer, primary_key=True)
    filename      = Column(Integer, unique=True)
    date_uploaded = Column(DateTime)

    def __init__(self, filename, date_uploaded):
        self.filename      = filename
        self.date_uploaded = date_uploaded

    def __repr__(self):
        return self.filename







