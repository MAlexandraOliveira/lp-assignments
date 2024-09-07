"""Tests for the cleaning module"""
import pandas as pd
from life_expectancy.cleaning import clean_data


def test_clean_data(input_sample_data, expected_sample_data):
    """Run the `clean_data` function and compare the output to the expected output"""
    cleaned_input_sample_data = clean_data(input_sample_data, 'AL')
   
    pd.testing.assert_frame_equal(
        cleaned_input_sample_data, expected_sample_data
    )