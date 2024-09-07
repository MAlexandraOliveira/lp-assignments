import pytest
from unittest import mock
from life_expectancy.main import run_all_functions
import pandas as pd


@mock.patch('life_expectancy.main.save_data')
@mock.patch('life_expectancy.main.clean_data')
@mock.patch('life_expectancy.main.load_data')
def test_process_data_success(mock_load_data, mock_clean_data, mock_save_data, expected_sample_data):
    # Mock the load_data to return a DataFrame
    mock_load_data.return_value = expected_sample_data

    # Mock the clean_data to return the same DataFrame (simplified for test)
    mock_clean_data.return_value = expected_sample_data

    # Call process_data
    run_all_functions(
        region="PT", 
        input_folder_path="data", 
        input_filename="eu_life_expectancy_raw.tsv", 
        output_folder_path="data", 
        output_filename="pt_life_expectancy.csv"
    )

    # Assert load_data, clean_data, and save_data were called with the expected values
    mock_load_data.assert_called_once_with("data", "eu_life_expectancy_raw.tsv")
    mock_clean_data.assert_called_once_with(expected_sample_data, "PT")
    mock_save_data.assert_called_once_with(expected_sample_data, "data", "pt_life_expectancy.csv")


@mock.patch('life_expectancy.main.save_data')
@mock.patch('life_expectancy.main.load_data')
def test_process_data_no_data(mock_load_data, mock_save_data):
    # Mock load_data to return None (no data)
    mock_load_data.return_value = None

    # Call process_data
    run_all_functions(
        region="PT", 
        input_folder_path="data", 
        input_filename="eu_life_expectancy_raw.tsv", 
        output_folder_path="data", 
        output_filename="pt_life_expectancy.csv"
    )

    # Assert load_data was called, but clean_data and save_data were not
    mock_load_data.assert_called_once_with("data", "eu_life_expectancy_raw.tsv")
    mock_save_data.assert_not_called()
