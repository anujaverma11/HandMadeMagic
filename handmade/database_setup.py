import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base # used for configuration and class code

from sqlalchemy.orm import relationship # to create Foreign Key relationships

from sqlalchemy import create_engine # used in configuration code at the end of the file.

Base = declarative_base() # Let SQL know that classes are special SQLAlchemy classes.


class Country(Base):
  __tablename__ = 'country'
  countryName = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)

class Region(Base):
  __tablename__ = 'region'
  cityName = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  country_id = Column(Integer, ForeignKey('country.id'))
  country = relationship(Country)

class Craft(Base):
  __tablename__ = 'craft'
  name = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)

class HandiCraft(Base):
  __tablename__ = 'handicraft'
  sub_craft = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  description = Column(String(250))
  region_id = Column(Integer, ForeignKey('region.id'))
  region = relationship(Region)
  craft_id = Column(Integer, ForeignKey('craft.id'))
  craft = relationship(Craft)

class Photo(Base):
  __tablename__ = 'photo'
  photoURL = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  handicraft_id = Column(Integer, ForeignKey('handicraft.id'))
  handicraft = relationship(HandiCraft)

class Video(Base):
  __tablename__ = 'video'
  videoURL = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  handicraft_id = Column(Integer, ForeignKey('handicraft.id'))
  handicraft = relationship(HandiCraft)

class Artist(Base):
  __tablename__='artist'
  name = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)

class Myart(Base):
  __tablename__='myart'
  title = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  artist_id = Column(Integer, ForeignKey('artist.id'))
  artist = relationship(Artist)
  handicraft_id = Column(Integer, ForeignKey('handicraft.id'))
  handicraft = relationship(HandiCraft)
  photo_id = Column(Integer, ForeignKey('photo.id'))
  photo = relationship(Photo)
  video_id = Column(Integer, ForeignKey('video.id'))
  video = relationship(Video)

engine = create_engine('sqlite:///handmade.db')
Base.metadata.create_all(engine)


