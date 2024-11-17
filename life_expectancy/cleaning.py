import re
import logging
from typing import Union
from abc import ABC, abstractmethod
import pandas as pd
from life_expectancy.data_structures import CombinedColumn, Region

Choosable = Union[str, int, float, bool, object]  

class BaseCleaningStrategy(ABC):
    """
    Abstract base class for data cleaning strategies.
    
    Defines the interface for cleaning DataFrames based on different strategies.
    """
    
    @abstractmethod
    def clean(self, df: pd.DataFrame, region: Region) -> pd.DataFrame:
        """
        Cleans the DataFrame according to the specific strategy.
        """
        pass

    def clean_year_column(self, data: pd.DataFrame) -> pd.DataFrame:
        """Processes the 'year' column by performing a set of operations."""
        data['year'] = data['year'].astype(str).str.strip()
        
        filtered_data = data[data['year'].str.isnumeric()]
        
        filtered_data['year'] = filtered_data['year'].astype(int)
        
        return filtered_data

    def remove_non_numeric_characters_from_column(self, 
                                                  data: pd.DataFrame, 
                                                  column_name: str) -> pd.Series:
        """Removes all non-numeric characters from a given column."""
        
        return data[column_name].apply(lambda x: re.sub(r'[^\d.]', '', str(x)))

    def clean_life_expectancy_values_column(self, data: pd.DataFrame, colname: str) -> pd.DataFrame:
        """Processes the column by performing a set of operations."""
        data.loc[:, colname] = self.remove_non_numeric_characters_from_column(data, colname)
        
        data.loc[:, colname] = pd.to_numeric(data[colname], errors='coerce')
        
        filtered_data = data.dropna(subset=[colname]).reset_index(drop=True)
        
        filtered_data[colname] = filtered_data[colname].astype('float64')
        
        return filtered_data

    def filter_data_by_region(self, 
                              data: pd.DataFrame, 
                              region: Region, 
                              colname: str) -> pd.DataFrame:
        """
        Filters the DataFrame by a given region.
        """
        filtered_data = data[data[colname] == region]
        
        return filtered_data.reset_index(drop=True)


class TSVCleaningStrategy(BaseCleaningStrategy):
    """
    Cleaning strategy for TSV (Tab-Separated Values) formatted data.

    Implements specific cleaning steps suitable for TSV data structures.
    """
    
    def clean(self, df: pd.DataFrame, region: Region) -> pd.DataFrame: 
        """
        Cleans the DataFrame according to the TSV cleaning strategy.
        """       
        try:
            splitted_data = self.split_combined_column(df)

            unpivoted_data = self.unpivot_dataframe(splitted_data)
            
            cleaned_year = self.clean_year_column(unpivoted_data)
            
            cleaned_value = self.clean_life_expectancy_values_column(cleaned_year, 'value')

            final_data = self.filter_data_by_region(cleaned_value, region, 'region')
                        
            return final_data
        
        except Exception as e:
            logging.error("Error during TSV cleaning: %s", e)
            raise

    def split_combined_column(self, data: pd.DataFrame) -> pd.DataFrame:
        """Splits the combined column into four separate columns: 
        'unit', 'sex', 'age', and 'region'."""
        # Create an instance of the CombinedColumn class
        combined_column = CombinedColumn()
        # Call the get_index_of_combined_column method on the instance
        index_value = combined_column.get_index_of_combined_column()
        
        data_split_columns = data.iloc[:, index_value].str.split(',', expand=True)
        
        data_split_columns.columns = pd.Index(['unit', 'sex', 'age', 'region'])
    
        # Drop the combined column from the original dataframe
        data_reduced = data.drop(columns=[data.columns[index_value]])   
        
        splitted_data = pd.concat([data_split_columns, data_reduced], axis=1)

        return splitted_data

    def unpivot_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """Unpivots the DataFrame to have 'year' and 'value' columns."""
        unpivoted_data = data.melt(id_vars=['unit', 'sex', 'age', 'region'],
                                   var_name='year',
                                   value_name='value')
        
        return unpivoted_data

class DefaultCleaningStrategy(BaseCleaningStrategy):
    """
    Default cleaning strategy for DataFrames.

    Implements standard cleaning steps without specialized processing.
    """
    
    def clean(self, df: pd.DataFrame, region: Region) -> pd.DataFrame:
        """
        Cleans the DataFrame according to the default cleaning strategy.
        """
        try:
            cleaned_year = self.clean_year_column(df)

            # Check if life_expectancy colum values contain non numeric characters
            non_numeric_values = df['life_expectancy'][
                pd.to_numeric(df['life_expectancy'], errors='coerce').isna()
                ]
            
            # If so, apply the function that removes them
            if not non_numeric_values.empty:
                cleaned_value = self.clean_life_expectancy_values_column(cleaned_year, 
                                                                    'life_expectancy')
            else:
                cleaned_value = cleaned_year.copy()
            
            final_data = self.filter_data_by_region(cleaned_value, region, 'country')
            
            return final_data
        
        except Exception as e:
            logging.error("Error during default cleaning: %s", e)
            
            raise


class DataCleaner:
    """
    Context class for data cleaning using different cleaning strategies.
    
    Allows switching between different cleaning strategies at runtime.
    """
    def __init__(self, strategy: BaseCleaningStrategy):
        """
        Initializes the DataCleaner with a specific cleaning strategy.
        """
        self.strategy = strategy

    def clean_data(self, df: pd.DataFrame, region: Region) -> pd.DataFrame:
        """
        Cleans the given DataFrame using the specified cleaning strategy.
        """
        return self.strategy.clean(df, region)
