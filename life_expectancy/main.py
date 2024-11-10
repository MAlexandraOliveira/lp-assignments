import argparse
import pandas as pd
from life_expectancy.load_data import load_data
from life_expectancy.cleaning import clean_data
from life_expectancy.save_data import save_data
from life_expectancy.data_structures import Region


def run_all_functions(region: Region, raw_data: pd.DataFrame, output_folder_path: str, 
                      output_filename: str):
    """Handles the main data processing steps: loading, cleaning, and saving."""
    cleaned_data = clean_data(raw_data, region)
    save_data(cleaned_data, output_folder_path, output_filename)


def main():
    """Runs all scripts."""
    parser = argparse.ArgumentParser(description="Process life expectancy data by region.")
    parser.add_argument('--region', type=str, default='PT',
                        help="The region to filter the data by. Default is 'PT'.")
    args = parser.parse_args()

    input_folder_path = 'data'
    input_filename = 'eu_life_expectancy_raw.tsv'
    
    # Create the Region enum dynamically
    raw_data = load_data(input_folder_path, input_filename)
    gen_regions = Region.generate_regions_dynamically(raw_data)

    user_region = args.region.upper()  

    if hasattr(gen_regions, user_region):
        region = getattr(gen_regions, user_region).value

        output_folder_path = 'data'
        output_filename = f'{args.region.lower()}_life_expectancy.csv'

        run_all_functions(region, raw_data, output_folder_path, output_filename)
    else:
        valid_regions = Region.get_actual_countries(raw_data)
        
        print(
                f"Error: The region {user_region} does not exist in the data. "
                f"Valid regions include: {', '.join(valid_regions)}."
            )


if __name__ == "__main__":
    main()
