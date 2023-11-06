# Import necessary libraries and modules
import click
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from alembic.config import Config
from alembic import command

# Define SQLAlchemy models
Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Diaper(Base):
    __tablename__ = 'diapers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))

    brand = relationship('Brand', back_populates='diapers')
    location = relationship('Location', back_populates='diapers')

Brand.diapers = relationship('Diaper', order_by=Diaper.id, back_populates='brand')
Location.diapers = relationship('Diaper', order_by=Diaper.id, back_populates='location')

# CLI commands and options (to be defined in a separate section)
