"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR


@pytest.fixture
def input_sample_data(scope="session")-> pd.DataFrame:
    """Fixture to load the expected sample input data for the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw.tsv", sep='\t')


@pytest.fixture
def expected_sample_data(scope="session")-> pd.DataFrame:
    """Fixture to load the expected sample output data of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected.csv")

