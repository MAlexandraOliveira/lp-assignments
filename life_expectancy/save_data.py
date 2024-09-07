import os
import pandas as pd
from life_expectancy.common_functions import get_base_directory


def save_data(data: pd.DataFrame, output_folder_path: str, output_filename: str) -> None:
    """Exports the DataFrame to a text file."""
    base_dir = get_base_directory()
    output_file_path = os.path.join(base_dir, output_folder_path, output_filename)
    data.to_csv(output_file_path, index=False)
