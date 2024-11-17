import pytest
import json
import zipfile
import pandas as pd
from life_expectancy.load_data import (
    DataLoaderContext,
    TSVDataLoader,
    JSONDataLoader,
    DataLoaderStrategy
)

from . import FIXTURES_DIR


@pytest.mark.parametrize("data_format", ["json", "tsv"])
def test_load_data_success(data_format, input_sample_data):
    """
    Tests if the success of the loading strategies
    """
    # Unpack data and file extension
    data, _ = input_sample_data
    
    input_folder_path = FIXTURES_DIR

    data_loader: DataLoaderStrategy
    
    if 'tsv' == data_format:
        input_filename = "eu_life_expectancy_raw.tsv"
        
        data_loader = TSVDataLoader()
    else:
        input_filename = "eurostat_life_expect.zip"
        
        data_loader = JSONDataLoader()

    context = DataLoaderContext(
            strategy=data_loader.load_data,
            input_folder_path=str(input_folder_path),
            input_filename=input_filename
        )
    loaded_data = context.load_data()

    # Assert that the loaded data matches the data from the fixture
    pd.testing.assert_frame_equal(loaded_data, data)


@pytest.mark.parametrize("data_loader_class, input_filename", [
    (TSVDataLoader, 'non_existent_file.tsv'),
    (JSONDataLoader, 'non_existent_file.zip'),
])
def test_load_data_file_not_found(data_loader_class, input_filename):
    """
    Test load_data() when the file is not found.
    Expect a FileNotFoundError to be raised.
    """
    input_folder_path = 'fake_folder'

    data_loader = data_loader_class()
    context = DataLoaderContext(
        strategy=data_loader.load_data,
        input_folder_path=input_folder_path,
        input_filename=input_filename
    )

    # Expecting a FileNotFoundError to be raised
    with pytest.raises(FileNotFoundError):
        context.load_data()


@pytest.mark.parametrize("data_loader_class, filename, expected_message", [
    (TSVDataLoader, 'empty_file.tsv', "Error: The file is empty."),
    (JSONDataLoader, 'empty_file.zip', "Error: There was an error decoding the JSON file."),
])
def test_load_data_empty_file(tmpdir, data_loader_class, filename, expected_message):
    """
    Test load_data() with an empty file.
    Expect a ValueError to be raised.
    """
    file_path = tmpdir.join(filename)
    
    if data_loader_class == JSONDataLoader:
        with zipfile.ZipFile(file_path, 'w') as zipf:
            zipf.writestr('empty_file.json', '')  # Empty JSON file inside zip
    else:
        file_path.write('')  # Empty TSV file

    input_folder_path = str(file_path.dirpath())
    input_filename = filename

    data_loader = data_loader_class()
    context = DataLoaderContext(
        strategy=data_loader.load_data,
        input_folder_path=input_folder_path,
        input_filename=input_filename
    )

    # Expecting a ValueError with the specific message
    with pytest.raises(ValueError, match=expected_message):
        context.load_data()


@pytest.mark.parametrize("data_loader_class, filename, malformed_content, expected_message", [
    (
        TSVDataLoader,
        'malformed_file.tsv',
        "col1|col2\nval1|val2\nval1\t",
        "Error: There was a parsing error while reading the file."
    ),
    (
        JSONDataLoader,
        'malformed_file.zip',
        '{"key1": "value1", "key2": "value2", "key1": }',  # Malformed JSON
        "Error: There was an error decoding the JSON file."
    ),
])
def test_load_data_parsing_error(tmpdir, data_loader_class, filename, malformed_content, expected_message):
    """
    Test load_data() with a malformed file.
    Expect a ValueError to be raised.
    """
    file_path = tmpdir.join(filename)
    
    if data_loader_class == JSONDataLoader:
        with zipfile.ZipFile(file_path, 'w') as zipf:
            zipf.writestr('malformed_file.json', malformed_content)
    else:
        file_path.write(malformed_content)

    input_folder_path = str(file_path.dirpath())
    input_filename = filename

    data_loader = data_loader_class()
    context = DataLoaderContext(
        strategy=data_loader.load_data,
        input_folder_path=input_folder_path,
        input_filename=input_filename
    )

    # Expecting a ValueError with a specific message
    with pytest.raises(ValueError, match=expected_message):
        context.load_data()
