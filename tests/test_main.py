# tests/test_main.py
# Import necessary modules for testing
import pytest
from lib.diaper_management import Location, Brand, Diaper, session
from click.testing import CliRunner
from lib.diaper_management import cli  # Import the Click CLI application

# Create a Click runner for testing
runner = CliRunner()

# Define a test for adding a location
def test_add_location():
    location_name = "Test Location"
    session.execute(f"DELETE FROM locations WHERE name = '{location_name}'")  # Delete if it already exists
    result = session.query(Location).filter_by(name=location_name).first()
    assert result is None  # Make sure the location doesn't exist initially

    # Call the CLI command to add a location
    result = runner.invoke(cli, ['add_location', '--location', location_name])

    assert result.exit_code == 0  # Check if the command ran successfully
    assert f'Location "{location_name}" added.' in result.output  # Check the output message

    # Check if the location now exists in the database
    result = session.query(Location).filter_by(name=location_name).first()
    assert result is not None  # Make sure the location was added successfully

# Define a test for adding a brand
def test_add_brand():
    brand_name = "Test Brand"
    session.execute(f"DELETE FROM brands WHERE name = '{brand_name}'")  # Delete if it already exists
    result = session.query(Brand).filter_by(name=brand_name).first()
    assert result is None  # Make sure the brand doesn't exist initially

    # Call the CLI command to add a brand
    result = runner.invoke(cli, ['add_brand', '--brand', brand_name])

    assert result.exit_code == 0  # Check if the command ran successfully
    assert f'Brand "{brand_name}" added.' in result.output  # Check the output message

    # Check if the brand now exists in the database
    result = session.query(Brand).filter_by(name=brand_name).first()
    assert result is not None  # Make sure the brand was added successfully

# Define a test for adding a diaper
def test_add_diaper():
    diaper_name = "Test Diaper"
    brand_id = 1  # Replace with an existing brand ID in your database
    location_id = 1  # Replace with an existing location ID in your database
    session.execute(f"DELETE FROM diapers WHERE name = '{diaper_name}'")  # Delete if it already exists
    result = session.query(Diaper).filter_by(name=diaper_name).first()
    assert result is None  # Make sure the diaper doesn't exist initially

    # Call the CLI command to add a diaper
    result = runner.invoke(cli, ['add_diaper', '--name', diaper_name, '--brand_id', brand_id, '--location_id', location_id])

    assert result.exit_code == 0  # Check if the command ran successfully
    assert f'Diaper "{diaper_name}" added to Location ID {location_id} and Brand ID {brand_id}.' in result.output  # Check the output message

    # Check if the diaper now exists in the database
    result = session.query(Diaper).filter_by(name=diaper_name).first()
    assert result is not None  # Make sure the diaper was added successfully

# Run the tests
if __name__ == '__main__':
    pytest.main()
