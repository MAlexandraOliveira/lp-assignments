import re
import os
import argparse
from typing import TypeVar, Optional
import pandas as pd

Choosable = TypeVar("Choosable", str, int, float, bool, object)


class RegionNotFoundError(ValueError):
    """Raised when a specified region is not found in the dataset."""
    def __init__(self, region: str, valid_regions: list):
        self.region = region
        self.valid_regions = valid_regions
        self.message = (f"Error: The region '{self.region}' does not exist in the data. "
                        f"Valid regions include: {', '.join(self.valid_regions[:5])}.")
        super().__init__(self.message)


def get_base_directory() -> str:
    """
    Determines the base directory where the script is located.
    """
    return os.path.dirname(os.path.abspath(__file__))


def load_data()-> Optional[pd.DataFrame]:
    """
    Loads a text file and raises exceptions if case something goes wrong.
    """
    # Construct the full path to the data file
    data_file_path = os.path.join(get_base_directory(), 'data', 'eu_life_expectancy_raw.tsv')

    try:
        data = pd.read_csv(data_file_path, sep='\t')
        print("TSV file loaded successfully!")
        
        return data
    except FileNotFoundError:
        print(f"Error: The file '{data_file_path}' was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: There was a parsing error while reading the file.")
    
    return None


def split_combined_column(data: pd.DataFrame) -> pd.DataFrame:
    """
    Splits the combined column into four separate columns: 'unit', 'sex', 'age', and 'region'.
    """
    data_split_columns = data.iloc[:, 0].str.split(',', expand=True)
    data_split_columns.columns = ['unit', 'sex', 'age', 'region']
    
    # Drop the combined column from the original dataframe
    data_reduced = data.drop(columns=[data.columns[0]])
    splitted_data = pd.concat([data_split_columns, data_reduced], axis=1)
    
    return splitted_data

    
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
    splitted_data = split_combined_column(data)
    new_data = unpivot_dataframe(splitted_data)
    
    return new_data


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
    filtered_data = filter_column_by_numeric_strings(data, 'year')
    filtered_data['year'] = change_column_type(filtered_data, 'year', int)
    
    return filtered_data


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
    filtered_data = remove_nan_by_column_subset(data, ['value'])
    filtered_data['value'] = change_column_type(filtered_data, 'value', float)
    
    return filtered_data


def filter_data_by_region(data: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Filter the DataFrame by a given region.
    Raises a RegionNotFoundError if the region does not exist in the data.

    Example:
    >>> filtered_data = filter_data_by_region(data, 'PT')
    """
    filtered_data = data[data['region'] == region]

    if filtered_data.empty:
        valid_regions = data['region'].unique().tolist()
        raise RegionNotFoundError(region, valid_regions)

    return filtered_data.reset_index(drop=True)


def clean_data(data: pd.DataFrame, region:str) -> pd.DataFrame:
    """
    Processes the input data, by formatting and filtering
    the original DataFrame and processing columns.
    """
    processed_data = process_data(data)
    processed_data_year_cleaned = clean_year_column(processed_data)
    processed_data_value_cleaned = clean_value_colum(processed_data_year_cleaned)
    final_data = filter_data_by_region(processed_data_value_cleaned, region)

    return final_data
   

def save_data(data: pd.DataFrame, region: str) -> None:
    """
    Exports the DataFrame to a text file.
    """
    base_dir = get_base_directory()
    output_file_path = os.path.join(base_dir, 'data', f'{region.lower()}_life_expectancy.csv')
    data.to_csv(output_file_path, index=False)


def run_all_functions(region: str) -> None:
    """
    Makes the functions call in order. This is the main function.
    """
    try:
        raw_data = load_data()
        if raw_data is not None:
            cleaned_data = clean_data(raw_data, region)
            save_data(cleaned_data, region)
    except RegionNotFoundError as e:
        print(e)


if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser(description="Process life expectancy data by region.")
    parser.add_argument('--region', type=str, default='PT',
                        help="The region to filter the data by. Default is 'PT'.")
    args = parser.parse_args()
    run_all_functions(args.region)

   
