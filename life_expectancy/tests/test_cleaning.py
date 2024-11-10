import os
import pandas as pd
from life_expectancy.cleaning import clean_data
from life_expectancy.data_structures import Region


def test_clean_data(input_sample_data, expected_sample_data):
    """Run the `clean_data` function and compare the output to the expected output"""
    gen_regions  = Region.generate_regions_dynamically(input_sample_data)
    
    region = getattr(gen_regions, 'AL', None)

    if region is None:
        raise ValueError("Region 'AL' not found in the generated enum.")

    cleaned_input_sample_data = clean_data(input_sample_data, region.value)
   
    pd.testing.assert_frame_equal(
        cleaned_input_sample_data, expected_sample_data
    )