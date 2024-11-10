import re
from typing import Union
import pandas as pd
from life_expectancy.data_structures import CombinedColumn, Region

Choosable = Union[str, int, float, bool, object]  


def split_combined_column(data: pd.DataFrame) -> pd.DataFrame:
    """Splits the combined column into four separate columns: 'unit', 'sex', 'age', and 'region'."""
    # Create an instance of the CombinedColumn class
    combined_column = CombinedColumn()
    # Call the get_index_of_combined_column method on the instance
    index_value = combined_column.get_index_of_combined_column()

    data_split_columns = data.iloc[:, index_value].str.split(',', expand=True)
    data_split_columns.columns = ['unit', 'sex', 'age', 'region']
   
    # Drop the combined column from the original dataframe
    data_reduced = data.drop(columns=[data.columns[index_value]])   
    splitted_data = pd.concat([data_split_columns, data_reduced], axis=1)
    
    return splitted_data

    
def unpivot_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Unpivots the DataFrame to have 'year' and 'value' columns."""
    unpivoted_data = data.melt(id_vars=['unit', 'sex', 'age', 'region'],
                               var_name='year',
                               value_name='value')
    return unpivoted_data


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the original DataFrame by splitting the combined column into four 
    columns and unpivoting the DataFrame.
    """
    splitted_data = split_combined_column(data)
    new_data = unpivot_dataframe(splitted_data)
    
    return new_data


def clean_year_column(data: pd.DataFrame) -> pd.DataFrame:
    """Processes the 'year' column by performing a set of operations."""
    data['year'] = data['year'].str.strip()
    filtered_data = data[data['year'].str.isnumeric()]
    filtered_data['year'] = filtered_data['year'].astype(int)
    
    return filtered_data


def remove_non_numeric_characters_from_column(data: pd.DataFrame, column_name: str) -> pd.Series:
    """Removes all non-numeric characters from a given column."""
    return data[column_name].apply(lambda x: re.sub(r'[^\d.]', '', str(x)))


def clean_value_column(data: pd.DataFrame) -> pd.DataFrame:
    """Processes the 'value' column by performing a set of operations."""
    data.loc[:, 'value'] = remove_non_numeric_characters_from_column(data, 'value')
    data.loc[:, 'value'] = pd.to_numeric(data['value'], errors='coerce')
    filtered_data = data.dropna(subset=['value']).reset_index(drop=True)
    filtered_data['value'] = filtered_data['value'].astype(float)
    
    return filtered_data


def filter_data_by_region(data: pd.DataFrame, region: Region) -> pd.DataFrame:
    """
    Filters the DataFrame by a given region.
    Raises a RegionNotFoundError if the region does not exist in the data.

    Example:
    >>> filtered_data = filter_data_by_region(data, 'PT')
    """
    filtered_data = data[data['region'] == region]
        
    return filtered_data.reset_index(drop=True)
    

def clean_data(data: pd.DataFrame, region: Region) -> pd.DataFrame:
    """
    Cleans the input data by transforming and filtering the original DataFrame 
    and processing its columns.
    """
    transformed_data = transform_data(data)
    transformed_data_year_cleaned = clean_year_column(transformed_data)
    transformed_data_value_cleaned = clean_value_column(transformed_data_year_cleaned)
    final_data = filter_data_by_region(transformed_data_value_cleaned, region)

    return final_data
