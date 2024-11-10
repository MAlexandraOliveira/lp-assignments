import pytest
import pandas as pd
from life_expectancy.load_data import load_data

from . import FIXTURES_DIR


def test_load_data_success(input_sample_data):
    input_folder_path = FIXTURES_DIR
    input_filename = "eu_life_expectancy_raw.tsv"

    # Call the function to load the data
    loaded_data = load_data(str(input_folder_path), input_filename)

    # Assert that the loaded data matches the data from the fixture
    pd.testing.assert_frame_equal(loaded_data, input_sample_data)


def test_load_data_file_not_found():
    """
    Test load_data() when the file is not found.
    Expect a FileNotFoundError to be raised.
    """
    input_folder_path = 'fake_folder'
    input_filename = 'non_existent_file.tsv'

    # Expecting a FileNotFoundError to be raised
    with pytest.raises(FileNotFoundError):
        load_data(input_folder_path, input_filename)


def test_load_data_empty_file(tmpdir):
    """
    Test load_data() with an empty file.
    Expect a pandas.errors.EmptyDataError to be raised.
    """
    # Use pytest's tmpdir fixture to create an empty file
    empty_file_path = tmpdir.mkdir("fixtures").join("empty_file.tsv")
    empty_file_path.write("")  # Create an empty file

    input_folder_path = str(empty_file_path.dirpath())
    input_filename = "empty_file.tsv"

    # Expecting an EmptyDataError to be raised
    with pytest.raises(pd.errors.EmptyDataError):
        load_data(input_folder_path, input_filename)


def test_load_data_parsing_error(tmpdir):
    """
    Test load_data() with a malformed TSV file.
    Expect a pandas.errors.ParserError to be raised.
    """
    # Use pytest's tmpdir fixture to create a malformed TSV file
    malformed_file_path = tmpdir.mkdir("fixtures").join("malformed_file.tsv")

    # Write malformed content that is likely to trigger a parsing error
    malformed_file_path.write("col1|col2\nval1|val2\nval1\t")  # Example of inconsistent row structure

    input_folder_path = str(malformed_file_path.dirpath())
    input_filename = "malformed_file.tsv"

    # Expecting a ParserError to be raised
    with pytest.raises(pd.errors.ParserError):
        load_data(input_folder_path, input_filename)