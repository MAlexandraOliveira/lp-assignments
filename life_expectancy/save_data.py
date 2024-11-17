import os
import logging
import pandas as pd
from life_expectancy.common_functions import get_base_directory

# Set up the logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
    ]
)

def save_data(data: pd.DataFrame, output_folder_path: str, output_filename: str) -> None:
    """Exports the DataFrame to a text file."""
    base_dir = get_base_directory()
    output_file_path = os.path.join(base_dir, output_folder_path, output_filename)
    
    try:
        # Check if the output folder path exists
        if not os.path.exists(os.path.join(base_dir, output_folder_path)):
            raise FileNotFoundError(
                f"The specified folder path '{output_folder_path}' does not exist.")
        
        # Save the DataFrame to a CSV file
        data.to_csv(output_file_path, index=False)
        
        # Log a success message
        logging.info("Data successfully saved to '%s'.", output_file_path)


    except FileNotFoundError as e:
        logging.error("Error: %s", e)
        raise

    except IOError as e:
        logging.error("Error saving data to '%s': %s", output_file_path, e)
        raise
    
