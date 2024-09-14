import os
import pandas as pd
from life_expectancy.load_data import load_data, get_base_directory
from life_expectancy.cleaning import clean_data
from life_expectancy.save_data import save_data
from life_expectancy.data_structures import Region


def create_input_sample_data(input_folder_path: str, input_filename: str) -> pd.DataFrame:
    """Creates a sample data from the original one for testing purposes"""
    raw_data = load_data(input_folder_path, input_filename)
    raw_data['Region'] = raw_data[raw_data.columns[0]].apply(lambda x: x.split(',')[-1])
    # Now filter the DataFrame where the Region is 'AL'
    df_sample = raw_data[(raw_data['Region'] == 'AL') | (raw_data['Region'] == 'PT')]

    # If you don't need the 'Region' column anymore, you can drop it
    df_sample = df_sample.drop(columns=['Region'])
    df_sample.to_csv(os.path.join(get_base_directory(), 'tests/fixtures', input_filename), 
                     sep='\t', index=False)

    return df_sample


def create_output_sample_data(data: pd.DataFrame, output_folder_path, output_filename)-> None:
    """Cleans and saves the sampled data for testing purposes"""
    gen_regions  = Region.generate_regions_dynamically(data)
    
    region = getattr(gen_regions, 'AL', None)

    if region is None:
        raise ValueError("Region 'AL' not found in the generated enum.")
    
    cleaned_data = clean_data(data, region.value)
    save_data(cleaned_data, output_folder_path, output_filename)


if __name__ == "__main__":
    input_folder_path, input_filename = 'data', 'eu_life_expectancy_raw.tsv'
    input_data = create_input_sample_data(input_folder_path, input_filename)
    
    output_folder_path, output_filename = 'tests/fixtures', 'eu_life_expectancy_expected.csv'
    create_output_sample_data(input_data, output_folder_path, output_filename)