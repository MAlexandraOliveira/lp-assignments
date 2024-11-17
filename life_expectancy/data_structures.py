from enum import Enum
from typing import List
from dataclasses import dataclass
import pandas as pd


@dataclass
class CombinedColumn:
    """Returns the index of the combined column of the DataFrame. 
    In case this index changes, you can modify it here
    """
    index_combined: int = 0

    def get_index_of_combined_column(self) -> int:
        """Return the index of the combined column"""
        return self.index_combined
   


class Region(Enum):
    """
    A dynamic enumeration class for country regions based on data extracted from a given file.

    This class provides methods to:
    - Extract unique regions from raw data.
    - Filter out non-country regions.
    - Dynamically generate a new Enum class for these regions.
    """

    @staticmethod
    def get_unique_regions_from_raw_data(raw_data: pd.DataFrame, file_format: str) -> List[str]:
        """
        Extracts a list of unique regions from the raw data.

        This method processes the first column of the input DataFrame, assuming it contains
        region data separated by commas, and extracts the last element (i.e., the region).
        It then returns a list of unique regions.
        """
        if raw_data is not None and not raw_data.empty:
            
            # Assuming the first column contains the region information separated by commas
            if 'tsv' == file_format:
                comb_col_idx = CombinedColumn().get_index_of_combined_column()
               
                raw_data['Region'] = raw_data[
                    raw_data.columns[comb_col_idx]].apply(lambda x: x.split(',')[-1])
            else:                
                raw_data = raw_data.rename(columns={'country': 'Region'})
            
            unique_regions = raw_data['Region'].unique().tolist()
            
            return unique_regions

        raise ValueError("The raw data provided is None or empty. Cannot generate regions.")

    @staticmethod
    def get_actual_countries(raw_data: pd.DataFrame, file_format: str) -> List[str]:
        """
        Filters and returns a list of actual countries, excluding non-country regions.

        This method uses the unique regions extracted from the raw data and removes
        any entries that represent non-country regions (e.g., regions with more than 2 characters).
        """
        unique_regions = Region.get_unique_regions_from_raw_data(raw_data, file_format)
        # Filtering regions by length, assuming country codes are 2 characters long
        actual_unique_regions = [item for item in unique_regions if len(item) <= 2]
        
        return actual_unique_regions

    @staticmethod
    def generate_regions_dynamically(raw_data: pd.DataFrame, file_format: str) -> Enum:
        """
        Dynamically generates an Enum class based on unique regions.

        This method creates an Enum class dynamically using the unique region names
        extracted from the raw data. The Enum class contains uppercase region names as 
        attributes and their corresponding original values.
        """
        unique_regions = Region.get_unique_regions_from_raw_data(raw_data, file_format)
        
        return Enum('Region', {value.upper(): value for value in unique_regions})
