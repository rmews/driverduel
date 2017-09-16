import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Driver(Base):
    __tablename__ = 'driver'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(String)
    picture = Column(String)

class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    track_type = Column(String)
    picture = Column(String)

class RaceResult(Base):
    __tablename__ = 'race_result'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    finish = Column(Integer)
    start = Column(Integer)
    laps_led = Column(Integer)
    fastest_laps = Column(Integer)
    points_finish = Column(Integer)
    points_differential = Column(Integer)
    points_led = Column(Numeric(4,2))
    points_fastest = Column(Numeric(4,2))
    points_total = Column(Numeric(4,2))
    driver_id = Column(Integer, ForeignKey('driver.id'))
    driver = relationship(Driver)
    track_id = Column(Integer, ForeignKey('track.id'))
    track = relationship(Track)

engine = create_engine('sqlite:///nascarstats.db')

Base.metadata.create_all(engine)
