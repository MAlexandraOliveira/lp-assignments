import pytest
import pandas as pd
from life_expectancy.cleaning import (
    DefaultCleaningStrategy,
    TSVCleaningStrategy,
    DataCleaner,
)
from life_expectancy.data_structures import Region


@pytest.mark.parametrize("data_format", ["json", "tsv"])
def test_clean_data(
    data_format,
    input_sample_data,
    expected_sample_data,
):
    """
    Run the `clean_data` function and compare the output to the expected output.
    """
    # Unpack the input data
    input_data, _ = input_sample_data  # data_format is already known

    # Generate regions dynamically based on the input data and data format
    gen_regions = Region.generate_regions_dynamically(input_data, data_format)

    # Specify the region code you want to test
    region_code = "AL"
    region = getattr(gen_regions, region_code, None)

    if region is None:
        raise ValueError(f"Region '{region_code}' not found in the generated regions.")

    # Select the appropriate cleaning strategy based on the data format
    if data_format == 'json':
        cleaning_strategy = DefaultCleaningStrategy()
    else:
        cleaning_strategy = TSVCleaningStrategy()

    # Initialize the DataCleaner with the selected strategy
    cleaner = DataCleaner(strategy=cleaning_strategy)

    # Clean the input data using the cleaner and the selected region
    cleaned_input_data = cleaner.clean_data(input_data, region.value)
   
    # Assert that the cleaned data matches the expected data
    pd.testing.assert_frame_equal(cleaned_input_data, expected_sample_data)
