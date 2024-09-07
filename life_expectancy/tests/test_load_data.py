import pytest
import pandas as pd
from life_expectancy.load_data import load_data

from . import FIXTURES_DIR


def test_load_data_success(input_sample_data):
    input_folder_path = FIXTURES_DIR
    input_filename = "eu_life_expectancy_raw.tsv"

    # Call the function to load the data
    loaded_data = load_data(input_folder_path, input_filename)

    # Assert that the loaded data matches the data from the fixture
    pd.testing.assert_frame_equal(loaded_data, input_sample_data)


def test_load_data_file_not_found():
    # Call the function with a non-existent file
    input_folder_path = 'fake_folder'
    input_filename = 'non_existent_file.tsv'

    # Expecting the function to return None due to FileNotFoundError
    data = load_data(input_folder_path, input_filename)
    assert data is None


def test_load_data_empty_file(tmpdir):
    # Use pytest's tmpdir fixture to create an empty file
    empty_file_path = tmpdir.mkdir("fixtures").join("empty_file.tsv")
    empty_file_path.write("")  # Create an empty file
    
    input_folder_path = str(empty_file_path.dirpath())
    input_filename = "empty_file.tsv"

    # Call the function, expecting None due to EmptyDataError
    data = load_data(input_folder_path, input_filename)
    assert data is None


def test_load_data_parsing_error(tmpdir):
    # Use pytest's tmpdir fixture to create a severely malformed TSV file
    malformed_file_path = tmpdir.mkdir("fixtures").join("malformed_file.tsv")
    
    # Write malformed content that is likely to trigger a parsing error
    # Example: Mixing separators or inconsistent row structure
    malformed_file_path.write("col1|col2\nval1|val2\nval1\t")

    input_folder_path = str(malformed_file_path.dirpath())
    input_filename = "malformed_file.tsv"

    # Call the function, expecting None due to a parsing error
    data = load_data(input_folder_path, input_filename)
    
    # Assert that the function returns None due to the parsing error
    assert data is None


