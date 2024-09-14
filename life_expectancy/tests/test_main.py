import pytest
import argparse
from unittest.mock import patch
from life_expectancy.main import main


@patch('life_expectancy.main.load_data')  
@patch('life_expectancy.main.clean_data')  
@patch('life_expectancy.main.save_data')  
@patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(region='AL'))  
def test_main(mock_parse_args, mock_save_data, mock_clean_data, mock_load_data, 
              input_sample_data, expected_sample_data):
    """
    Test the main function by mocking the calls to external modules and command-line arguments,
    and using fixtures for input and cleaned data.
    """
    # Setup mock return values for external functions
    mock_load_data.return_value = input_sample_data  
    mock_clean_data.return_value = expected_sample_data  
    mock_save_data.return_value = True  

    main()

    # Assert that each function was called
    mock_load_data.assert_called_once()
    mock_clean_data.assert_called_once_with(input_sample_data, 'AL')  
    mock_save_data.assert_called_once()

    # Optionally, check the call arguments
    mock_save_data.assert_called_once_with(expected_sample_data, 'data', 'al_life_expectancy.csv')
