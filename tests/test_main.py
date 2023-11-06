# tests/test_main.py

# Import the necessary functions from your main.py
from main import add_location

def test_add_location():
    # Initialize a database session and engine for testing
    # You should replace this with your database configuration
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    db_engine = create_engine('sqlite:///test_db.db')
    Session = sessionmaker(bind=db_engine)
    session = Session()

    # Call the function with a sample location name
    add_location('TestLocation', session)

    # Retrieve the added location from the database
    added_location = session.query(Location).filter_by(name='TestLocation').first()

    # Assert that the location has been added
    assert added_location is not None
    assert added_location.name == 'TestLocation'

    # Clean up (close the session)
    session.close()
