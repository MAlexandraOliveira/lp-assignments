import argparse
import sys
import logging
from typing import Tuple
import pandas as pd

from life_expectancy.cleaning import (
    BaseCleaningStrategy,
    DefaultCleaningStrategy,
    TSVCleaningStrategy,
    DataCleaner,
)
from life_expectancy.save_data import save_data
from life_expectancy.data_structures import Region
from life_expectancy.load_data import (
    DataLoaderContext,
    TSVDataLoader,
    JSONDataLoader,
    DataLoaderStrategy
)


def arguments_processor() -> argparse.Namespace:
    """
    Parses command-line arguments for the script.
    """
    parser = argparse.ArgumentParser(
                        description="Process life expectancy data by region.",
                        epilog="Example usage: python main.py --region PT --format csv"
                                    )
    
    parser.add_argument(
                        '--region', 
                        type=str, 
                        default='PT',
                        help="The region to filter the data by. Default is 'PT'.")
    
    parser.add_argument(
                        '--format', 
                        type=str, 
                        choices=['tsv', 'json'], 
                        default='tsv',
                        help="The format of the input data file."
                        "Choices are 'tsv' or 'json'. Default is 'tsv'.")
    
    args = parser.parse_args()

    return args


def get_data(args: argparse.Namespace, 
             input_folder_path: str) -> Tuple[pd.DataFrame, BaseCleaningStrategy]:
    """
    Loads raw data and selects the appropriate cleaning strategy based on the file format.
    """
    
    if args.format == 'json':
        input_filename = 'eurostat_life_expect.zip'
    elif args.format == 'tsv':
        input_filename = 'eu_life_expectancy_raw.tsv'
    else:
        logging.error("Unsupported file format: %s", args.format)
        sys.exit(1)
        
    try:
        data_loader: DataLoaderStrategy
        cleaning_strategy: BaseCleaningStrategy

        if args.format == 'json':
            data_loader = JSONDataLoader()
            cleaning_strategy = DefaultCleaningStrategy()
        elif args.format == 'tsv':
            data_loader = TSVDataLoader()
            cleaning_strategy = TSVCleaningStrategy()
        else:
            logging.error("Unsupported file format: %s", args.format)
            sys.exit(1)
        
        context = DataLoaderContext(
            strategy=data_loader.load_data,
            input_folder_path=input_folder_path,
            input_filename=input_filename
        )
        raw_data = context.load_data()
        logging.info("Data loaded successfully.")

        return raw_data, cleaning_strategy
    
    except (IOError, ValueError) as e:
        logging.error("Failed to load data: %s", e)
        sys.exit(1)


def process_and_export_data(args: argparse.Namespace, 
                            raw_data: pd.DataFrame, 
                            cleaning_strategy: BaseCleaningStrategy) -> None:
    """
    Processes the raw data for the specified region and exports the cleaned data.
    """
    try:
        gen_regions = Region.generate_regions_dynamically(raw_data, args.format)
    except (AttributeError, KeyError) as e:
        logging.error("Failed to generate regions: %s", e)
        sys.exit(1)
        
    user_region = args.region.upper()
    
    if hasattr(gen_regions, user_region):
        try:
            region = getattr(gen_regions, user_region).value
            
            output_folder_path = 'data'
            
            output_filename = f'{args.region.lower()}_life_expectancy.csv'
            
            # Initialize the cleaner with the selected strategy
            cleaner = DataCleaner(strategy=cleaning_strategy)
            
            cleaned_data = cleaner.clean_data(raw_data, region)

            # Save the data
            save_data(cleaned_data, output_folder_path, output_filename)
            
            logging.info("Data cleaned and saved successfully.")
        
        except (IOError, ValueError) as e:
            logging.error("Failed to process and save data: %s", e)
            sys.exit(1)
    else:
        valid_regions = Region.get_actual_countries(raw_data, args.format)
        print(
            f"Error: The region '{user_region}' does not exist in the data.\n"
            f"Valid regions include: {', '.join(valid_regions)}."
        )
        sys.exit(1)




def main():
    """
    Runs all scripts.
    """
    args = arguments_processor()
    
    input_folder_path = 'data'
    
    raw_data, cleaning_strategy = get_data(args, input_folder_path)
    
    process_and_export_data(args, raw_data, cleaning_strategy)
    

if __name__ == "__main__": # pragma: no cover
    main()
