import argparse
from life_expectancy.load_data import load_data
from life_expectancy.cleaning import clean_data
from life_expectancy.save_data import save_data
from life_expectancy.data_structures import RegionNotFoundError


def run_all_functions(region: str, input_folder_path: str, input_filename: str, output_folder_path: str, output_filename: str):
    """Handles the main data processing steps: loading, cleaning, and saving."""
    raw_data = load_data(input_folder_path, input_filename)

    if raw_data is not None:
        cleaned_data = clean_data(raw_data, region)
        save_data(cleaned_data, output_folder_path, output_filename)


def main():
    """Runs all scripts."""
    parser = argparse.ArgumentParser(description="Process life expectancy data by region.")
    parser.add_argument('--region', type=str, default='PT',
                        help="The region to filter the data by. Default is 'PT'.")
    args = parser.parse_args()

    try:
        input_folder_path = 'data'
        input_filename = 'eu_life_expectancy_raw.tsv'
        output_folder_path = 'data'
        output_filename = f'{args.region.lower()}_life_expectancy.csv'

        run_all_functions(args.region, input_folder_path, input_filename, output_folder_path, output_filename)
    except RegionNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()