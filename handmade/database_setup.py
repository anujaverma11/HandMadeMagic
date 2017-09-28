import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base # used for configuration and class code

from sqlalchemy.orm import relationship # to create Foreign Key relationships

from sqlalchemy import create_engine # used in configuration code at the end of the file.

Base = declarative_base() # Let SQL know that classes are special SQLAlchemy classes.

class MyArt(Base):
  __tablename__='myart'
  name = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)

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

class Category(Base):
  __tablename__ = 'category'
  name = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)

class HandiCraft(Base):
  __tablename__ = 'handicraft'
  sub_category = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  description = Column(String(250))
  region_id = Column(Integer, ForeignKey('region.id'))
  region = relationship(Region)
  category_id = Column(Integer, ForeignKey('category.id'))
  category = relationship(Category)

class Photo(Base):
  __tablename__ = 'photo'
  photoURL = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  handicraft_id = Column(Integer, ForeignKey('handicraft.id'))
  handicraft = relationship(HandiCraft)

class Video(Base):
  __tablename__ = 'video'
  VideoURL = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  handicraft_id = Column(Integer, ForeignKey('handicraft.id'))
  handicraft = relationship(HandiCraft)


engine = create_engine('sqlite:///handmade.db')
Base.metadata.create_all(engine)
