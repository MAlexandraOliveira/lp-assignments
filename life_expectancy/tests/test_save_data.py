import os
import pytest
import pandas as pd
from life_expectancy.save_data import save_data


def test_save_data_success(tmpdir, expected_sample_data):
    # Use the fixture `expected_sample_data` for the DataFrame to save
    df = expected_sample_data

    # Create a temporary directory and filename to save the data
    output_folder_path = tmpdir.mkdir("fixtures")
    output_filename = "test_output.csv"

    # Call save_data
    save_data(df, str(output_folder_path), output_filename)

    # Check if the file was created
    output_file_path = os.path.join(str(output_folder_path), output_filename)
    assert os.path.exists(output_file_path)

    # Read the file back and verify its content
    loaded_df = pd.read_csv(output_file_path)
    pd.testing.assert_frame_equal(df, loaded_df)


def test_save_data_invalid_path(expected_sample_data):
    # Use the fixture `expected_sample_data` for the DataFrame to save
    df = expected_sample_data

    # Use an invalid folder path
    invalid_folder_path = "/invalid/folder/path"
    output_filename = "test_output.csv"

    # Call save_data and expect it to raise an OSError due to invalid path
    with pytest.raises(OSError):
        save_data(df, invalid_folder_path, output_filename)

