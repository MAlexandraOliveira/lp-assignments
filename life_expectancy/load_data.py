import os
import logging
import pandas as pd
from life_expectancy.common_functions import get_base_directory


logging.basicConfig(level=logging.ERROR)


def load_data(input_folder_path: str, input_filename: str) -> pd.DataFrame:
    """Loads a text file and raises exceptions if case something goes wrong."""
    data_file_path = os.path.join(get_base_directory(), input_folder_path, input_filename)
    
    try:
        data = pd.read_csv(data_file_path, sep='\t')
        print("TSV file loaded successfully!")
               
        return data
    except FileNotFoundError:
        logging.error("Error: The file %s was not found.", data_file_path)
        raise
    except pd.errors.EmptyDataError:
        logging.error("Error: The file is empty.")
        raise
    except pd.errors.ParserError:
        logging.error("Error: There was a parsing error while reading the file.")
        raise
    
