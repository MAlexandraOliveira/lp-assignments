import pandas as pd
import pytest
from life_expectancy.data_structures import Region

def test_get_actual_countries():
    # Sample DataFrame to test with some regions and non-country regions
    raw_data = pd.DataFrame({
        'Region_Code': ['AL', 'AM', 'EU28', 'FX', 'US', 'EU27_2020', 'PT']
    })
    
    # Call the get_actual_countries method
    actual_countries = Region.get_actual_countries(raw_data)
    
    # Expected countries (only those with 2-character codes)
    expected_countries = ['AL', 'AM', 'FX', 'US', 'PT']
    
    # Assert that the method returns only the actual countries
    assert actual_countries == expected_countries, "The actual countries list is incorrect"


def test_get_unique_regions_from_raw_data(input_sample_data):
    """
    Test get_unique_regions_from_raw_data() to ensure it returns the correct unique regions.
    """
    # Call the static method with the input sample data
    unique_regions = Region.get_unique_regions_from_raw_data(input_sample_data)
    
    # Expected output based on the sample data in the fixture
    expected_regions = ['AL', 'PT']  

    # Assert that the returned regions match the expected output
    assert set(unique_regions) == set(expected_regions), f"Expected {expected_regions}, but got {unique_regions}"

