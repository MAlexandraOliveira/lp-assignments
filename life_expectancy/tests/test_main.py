import pytest
import argparse
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
from life_expectancy.main import main
from life_expectancy.common_functions import get_base_directory


@pytest.mark.parametrize("data_format", ["json", "tsv"])
@patch('life_expectancy.main.save_data')
@patch('life_expectancy.main.DataCleaner')
@patch('life_expectancy.main.JSONDataLoader')
@patch('life_expectancy.main.TSVDataLoader')
@patch('life_expectancy.main.Region')
@patch('argparse.ArgumentParser.parse_args')
def test_main(
    mock_parse_args,
    mock_region,
    mock_tsv_loader,
    mock_json_loader,
    mock_data_cleaner,
    mock_save_data,
    input_sample_data,
    expected_sample_data,
    data_format
):
    """
    Test the main function by mocking external dependencies and command-line arguments,
    and using fixtures for input and cleaned data, for both JSON and TSV formats.
    """
    # Setup mock command-line arguments
    mock_parse_args.return_value = argparse.Namespace(region='AL', format=data_format)

    # Extract input data from the fixture
    input_data, _ = input_sample_data
    cleaned_data = expected_sample_data

    # Mock the appropriate DataLoader based on the data_format
    mock_loader = mock_json_loader if data_format == "json" else mock_tsv_loader
    mock_loader.return_value.load_data.return_value = input_data

    # Mock Region to dynamically generate regions
    mock_generated_regions = MagicMock()
    mock_generated_regions.AL.value = 'AL'
    mock_region.generate_regions_dynamically.return_value = mock_generated_regions

    # Mock DataCleaner to clean data
    mock_cleaner_instance = MagicMock()
    mock_cleaner_instance.clean_data.return_value = cleaned_data
    mock_data_cleaner.return_value = mock_cleaner_instance

    # Mock save_data to ensure it is called without actually saving data
    mock_save_data.return_value = True

    # Determine full input file path
    base_dir = get_base_directory()
    input_folder_path = Path(os.path.join(base_dir, 'data'))
    input_filename = 'eurostat_life_expect.zip' if data_format == 'json' else 'eu_life_expectancy_raw.tsv'
    full_file_path = str(input_folder_path / input_filename)

    # Execute the main function
    main()

    # Assertions for data loading
    mock_loader.return_value.load_data.assert_called_once_with(full_file_path)

    # Assertions for region generation and cleaning
    mock_region.generate_regions_dynamically.assert_called_once_with(input_data, data_format)
    mock_data_cleaner.assert_called_once()
    mock_cleaner_instance.clean_data.assert_called_once_with(input_data, 'AL')

    # Assertions for saving the cleaned data
    mock_save_data.assert_called_once_with(cleaned_data, 'data', 'al_life_expectancy.csv')
