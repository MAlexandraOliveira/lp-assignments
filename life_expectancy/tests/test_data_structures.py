import pandas as pd
import pytest
from life_expectancy.data_structures import Region


@pytest.mark.parametrize("data_format, expected_countries", [
    ("tsv", ['AL', 'AM', 'FX', 'US', 'PT']),
    ("json", ['AL', 'AM', 'FX', 'US', 'PT']),
    # Add more formats if necessary
])
def test_get_actual_countries(data_format, expected_countries):
    """
    Test get_actual_countries() to ensure it filters valid regions on the dataset.
    """
    # Sample DataFrame to test with some regions and non-country regions
    raw_data = pd.DataFrame({
        'country': ['AL', 'AM', 'EU28', 'FX', 'US', 'EU27_2020', 'PT']
    })
    
    # Call the get_actual_countries method
    actual_countries = Region.get_actual_countries(raw_data.copy(), data_format)
    
    # Assert that the method returns only the actual countries
    assert actual_countries == expected_countries, "The actual countries list is incorrect"


@pytest.mark.parametrize("data_format", ["json", "tsv"])
def test_get_unique_regions_from_raw_data(data_format, input_sample_data):
    """
    Test get_unique_regions_from_raw_data() to ensure it returns the correct unique regions.
    """
    # Expected output based on the sample data in the fixture
    expected_regions = ['AL', 'PT']

    # Unpack data and file extension
    data, _ = input_sample_data

    # Call the static method with the input sample data
    unique_regions = Region.get_unique_regions_from_raw_data(data, data_format)

    # Assert that the returned regions match the expected output
    assert set(unique_regions) == set(expected_regions), f"Expected {expected_regions}, but got {unique_regions}"
