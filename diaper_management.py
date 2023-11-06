# Import necessary libraries and modules
import click
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from alembic.config import Config
from alembic import command
import click

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

# CLI commands and options

@click.group()
def cli():
    pass

@cli.command()
@click.option('--location', prompt='Enter location name', help='Name of the location')
def add_location(location):
    # Add a new location to the database
    new_location = Location(name=location)
    session.add(new_location)
    session.commit()
    click.echo(f'Location "{location}" added.')

@cli.command()
@click.option('--brand', prompt='Enter brand name', help='Name of the brand')
def add_brand(brand):
    # Add a new diaper brand to the database
    new_brand = Brand(name=brand)
    session.add(new_brand)
    session.commit()
    click.echo(f'Brand "{brand}" added.')

@cli.command()
@click.option('--name', prompt='Enter diaper name', help='Name of the diaper')
@click.option('--brand_id', type=int, prompt='Enter brand ID', help='ID of the brand')
@click.option('--location_id', type=int, prompt='Enter location ID', help='ID of the location')
def add_diaper(name, brand_id, location_id):
    # Add a new diaper to the database
    new_diaper = Diaper(name=name, brand_id=brand_id, location_id=location_id)
    session.add(new_diaper)
    session.commit()
    click.echo(f'Diaper "{name}" added to Location ID {location_id} and Brand ID {brand_id}.')

@cli.command()
@click.option('--location', prompt='Enter location name', help='Name of the location')
def list_diapers(location):
    # List diapers available in a specific location
    location_obj = session.query(Location).filter_by(name=location).first()
    if location_obj:
        diapers = location_obj.diapers
        for diaper in diapers:
            click.echo(f'Diaper Name: {diaper.name}, Brand: {diaper.brand.name}')
    else:
        click.echo(f'Location "{location}" not found.')

# Database configuration using Alembic
alembic_cfg = Config("alembic.ini")

@cli.command()
def upgrade_db():
    # Apply Alembic migrations to upgrade the database
    command.upgrade(alembic_cfg, 'head')
    click.echo('Database migration completed.')

@cli.command()
def downgrade_db():
    # Apply Alembic migrations to downgrade the database
    command.downgrade(alembic_cfg, '-1')
    click.echo('Database migration rollback completed.')

if __name__ == '__main__':
    cli()

# Configure the database engine (replace 'sqlite:///diaper_management.db' with your database URL)
db_engine = create_engine('sqlite:///diaper_management.db')
Base.metadata.create_all(db_engine)

# Create a session to interact with the database
Session = sessionmaker(bind=db_engine)
session = Session()

cli()