from dataclasses import dataclass
from typing import Protocol, Callable
import json
import os
import zipfile
import pandas as pd
from life_expectancy.common_functions import get_base_directory


def handle_errors(func):
    """
    Decorator to handle common file loading errors such as FileNotFound, 
    EmptyData, and Parsing errors.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as exc:
            # Attempt to extract 'file_path' from kwargs or args
            file_path = kwargs.get('file_path')
            
            if not file_path and len(args) >= 2:
                file_path = args[1]  # args[0] is 'self', args[1] is 'file_path'
            else:
                file_path = 'unknown'

            raise FileNotFoundError(f"Error: The file '{file_path}' was not found.") from exc
        except pd.errors.EmptyDataError as exc:
            raise ValueError("Error: The file is empty.") from exc
        except pd.errors.ParserError as exc:
            raise ValueError("Error: There was a parsing error while reading the file.") from exc
        except json.JSONDecodeError as exc:
            raise ValueError("Error: There was an error decoding the JSON file.") from exc

    return wrapper


class DataLoaderStrategy(Protocol):
    """
    Protocol for data loader strategy classes.
    Defines the interface for loading data from different file formats.
    """
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Cleans the DataFrame according to the specific strategy.
        """
        ...


class TSVDataLoader:
    """
    Data loader for CSV (Comma Separated Values) files.
    """
    @handle_errors
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Loads the data from a tsv file
        """
        data = pd.read_csv(file_path, sep='\t')
        print("TSV file loaded successfully!")
        
        return data


class JSONDataLoader:
    """
    Data loader for JSON files inside a ZIP archive.
    """
    @handle_errors
    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Loads the data from a zip file that contains a json file
        """
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            namelist = zip_file.namelist()
        
            if not namelist:
                raise ValueError("Error: The ZIP archive is empty.")
            json_filename = namelist[0]  
            with zip_file.open(json_filename) as json_file:
                data_dict = json.load(json_file)
                data = pd.DataFrame(data_dict)
                
                print("JSON file loaded successfully from ZIP!")
                
                return data

   
@dataclass
class DataLoaderContext:
    """
    Context class for using different data loading strategies.
    This class accepts a strategy to load data from a specified file format.
    """
    strategy: Callable[[str], pd.DataFrame]
    input_folder_path: str
    input_filename: str

    def load_data(self) -> pd.DataFrame:
        """
        Load data using the specified strategy from the given folder path and filename.

        :return: A pandas DataFrame containing the loaded data.
        """
        base_directory = get_base_directory()  
        file_path = os.path.join(base_directory, self.input_folder_path, self.input_filename)
        
        return self.strategy(file_path)
