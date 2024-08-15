import re
import os
import argparse
from typing import TypeVar, Optional
import pandas as pd

Choosable = TypeVar("Choosable", str, int, float, bool, object)

def read_data(file_path: str)-> Optional[pd.DataFrame]:
    """
    Imports and reads a text file and raises exceptions if case something goes wrong.
    """
    try:
        data = pd.read_csv(file_path, sep='\t')
        print("TSV file read successfully!")
        
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a parsing error while reading the file.")
    
    return None


def split_combined_column(data: pd.DataFrame) -> pd.DataFrame:
    """
    Splits the combined column into four separate columns: 'unit', 'sex', 'age', and 'region'.
    """
    split_columns = data.iloc[:, 0].str.split(',', expand=True)
    split_columns.columns = ['unit', 'sex', 'age', 'region']
    data = data.drop(columns=[data.columns[0]])
    data = pd.concat([split_columns, data], axis=1)
    
    return data


def unpivot_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """
    Unpivots the DataFrame to have 'year' and 'value' columns.
    """
    unpivoted_data = data.melt(id_vars=['unit', 'sex', 'age', 'region'],
                               var_name='year',
                               value_name='value')
    return unpivoted_data


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the DataFrame by splitting the combined column and then unpivoting the DataFrame.
    """
    data = split_combined_column(data)
    data = unpivot_dataframe(data)
    
    return data


def remove_column_spaces(data: pd.DataFrame, column_name: str) -> pd.Series:
    """
    Remove the spaces the might exist in the column's values.
    """
    return data[column_name].str.strip()


def filter_column_by_numeric_strings(data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Filter the DataFrame by the column values that are numeric.
    """
    return data[data[column_name].str.isnumeric()]


def change_column_type(data: pd.DataFrame, column_name: str, data_type: Choosable) -> pd.Series:
    """
    Cast a given column to a given data type.
    """
    return data[column_name].astype(data_type)


def clean_year_column(data: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the 'year' column by performing a set of operations.
    """
    data['year'] = remove_column_spaces(data, 'year')
    data = filter_column_by_numeric_strings(data, 'year')
    data['year'] = change_column_type(data, 'year', int)
    
    return data


def remove_non_numeric_characteres_from_column(data: pd.DataFrame, column_name: str) -> pd.Series:
    """
    Remove all non numeric characters from a given column.
    """
    return data[column_name].apply(lambda x: re.sub(r'[^\d.]', '', str(x)))


def convert_column_to_numeric(data: pd.DataFrame, column_name: str) -> pd.Series:
    """
    Convert a given column to numeric and convert to NaN non numerical values.
    """
    return pd.to_numeric(data[column_name], errors='coerce')


def remove_nan_by_column_subset(data: pd.DataFrame, column_subset: list[str]) -> pd.DataFrame:
    """
    Remove rows from a DataFrame based on the rows with NaN of a given subset of columns.
    """
    return data.dropna(subset=column_subset).reset_index(drop=True)


def clean_value_colum(data: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the 'value' column by performing a set of operations.
    """
    data['value'] = remove_non_numeric_characteres_from_column(data, 'value')
    data['value'] = convert_column_to_numeric(data, 'value')
    data = remove_nan_by_column_subset(data, ['value'])
    data['value'] = change_column_type(data, 'value', float)
    
    return data

def filter_data_by_region(data: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Filter the DataFrame by a given region.
    """
    return data[data['region'] == region].reset_index(drop=True)


def export_data(data: pd.DataFrame, file_path: str) -> None:
    """
    Exports the DataFrame to a text file.
    """
    data.to_csv(file_path, index=False)


def clean_data(region:str) -> None:
    """
    Processes the input data, by formatting and filtering
    the original DataFrame and processing columns.
    """
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the data file
    data_file_path = os.path.join(base_dir, 'data', 'eu_life_expectancy_raw.tsv')
    data = read_data(data_file_path)
    
    new_data = process_data(data)
    new_data = clean_year_column(new_data)
    new_data = clean_value_colum(new_data)
    new_data = filter_data_by_region(new_data, region)
    
    output_file_path = os.path.join(base_dir, 'data', f'{region.lower()}_life_expectancy.csv')
    export_data(new_data, output_file_path)


if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser(description="Process life expectancy data by region.")
    parser.add_argument('--region', type=str, default='PT',
                        help="The region to filter the data by. Default is 'PT'.")
    args = parser.parse_args()
    clean_data(args.region)
