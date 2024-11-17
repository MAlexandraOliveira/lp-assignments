"""Pytest configuration file"""
import zipfile
import json
import pandas as pd
import pytest
from typing import Tuple

from . import FIXTURES_DIR


@pytest.fixture
def input_sample_data(data_format) -> Tuple[pd.DataFrame, str]:
    """Fixture to load the sample input data for the cleaning script."""
    if data_format == 'tsv':
        data = pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep='\t')
    elif data_format == 'json':
        with zipfile.ZipFile(FIXTURES_DIR / "eurostat_life_expect.zip", 'r') as zip_file:
            json_filename = zip_file.namelist()[0]
            with zip_file.open(json_filename) as json_file:
                data_dict = json.load(json_file)
                data = pd.DataFrame(data_dict)
    else:
        raise ValueError("Unsupported data format")

    return data, data_format


@pytest.fixture
def expected_sample_data(data_format) -> pd.DataFrame:
    """Fixture to load the expected output data for the cleaning script."""
    if data_format == 'tsv':
        data = pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")
    elif data_format == 'json':
        data = pd.read_csv(FIXTURES_DIR / "eurostat_life_expect.csv", 
                           na_values=[], keep_default_na=False)
        data = data.replace('<<NONE>>', None)
    else:
        raise ValueError("Unsupported data format")

    return data
