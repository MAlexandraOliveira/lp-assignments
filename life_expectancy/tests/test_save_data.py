import os
import pytest
import pandas as pd
from life_expectancy.save_data import save_data


@pytest.mark.parametrize("data_format", ["json", "tsv"])
def test_save_data_success(tmpdir, expected_sample_data, data_format):
    # Use the fixture `expected_sample_data` for the DataFrame to save
    df = expected_sample_data

    # Create a temporary directory and filename to save the data
    output_folder_path = tmpdir.mkdir("fixtures")
    output_filename = "test_output.csv"

    # Call save_data
    save_data(df, str(output_folder_path), output_filename)

    # Check if the file was created
    output_file_path = os.path.join(str(output_folder_path), output_filename)
    assert os.path.exists(output_file_path), f"File {output_file_path} does not exist."

    # Read the file back and verify its content
    if 'json' == data_format:
        loaded_df = pd.read_csv(output_file_path, na_values=[], keep_default_na=False)
        loaded_df['flag_detail'] = loaded_df['flag_detail'].replace('', None)
    else:
        loaded_df = pd.read_csv(output_file_path)
    
    pd.testing.assert_frame_equal(df, loaded_df)


@pytest.mark.parametrize("data_format", ["json", "tsv"])
def test_save_data_folder_not_exist(expected_sample_data, data_format):
    # Use the fixture `expected_sample_data` for the DataFrame to save
    df = expected_sample_data

    # Use a non-existent folder path
    non_existent_folder_path = "non_existent_folder"
    output_filename = "test_output.csv"

    # Call save_data and expect it to raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        save_data(df, non_existent_folder_path, output_filename)


@pytest.mark.parametrize("data_format", ["json", "tsv"])
def test_save_data_io_error(tmpdir, expected_sample_data, data_format, monkeypatch):
    # Use the fixture `expected_sample_data` for the DataFrame to save
    df = expected_sample_data

    # Create a temporary directory and filename to save the data
    output_folder_path = tmpdir.mkdir("fixtures")
    output_filename = "test_output.csv"
    output_file_path = os.path.join(str(output_folder_path), output_filename)

    # Simulate an IOError by monkeypatching pandas.DataFrame.to_csv
    def mock_to_csv(*args, **kwargs):
        raise IOError("Simulated IOError")

    monkeypatch.setattr(pd.DataFrame, "to_csv", mock_to_csv)

    # Call save_data and expect it to raise an IOError
    with pytest.raises(IOError):
        save_data(df, str(output_folder_path), output_filename)
