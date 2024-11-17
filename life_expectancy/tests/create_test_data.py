import os
import json
import zipfile
from io import BytesIO
import pandas as pd
from life_expectancy.load_data import (DataLoaderStrategy, 
                                       TSVDataLoader, 
                                       JSONDataLoader,
                                       DataLoaderContext)
from life_expectancy.cleaning import (BaseCleaningStrategy, 
                                      TSVCleaningStrategy, 
                                      DefaultCleaningStrategy,
                                      DataCleaner)
from life_expectancy.common_functions import get_base_directory
from life_expectancy.save_data import save_data
from life_expectancy.data_structures import Region


def create_input_sample_data(input_folder_path: str, 
                             input_filename: str,
                             file_format: str) -> pd.DataFrame:
    """Creates a sample data from the original one for testing purposes"""
    data_loader: DataLoaderStrategy

    if file_format == 'json':
        data_loader = JSONDataLoader()
    elif file_format == 'tsv':
        data_loader = TSVDataLoader()

    context = DataLoaderContext(
            strategy=data_loader.load_data,
            input_folder_path=input_folder_path,
            input_filename=input_filename
        )
    
    raw_data = context.load_data()
    
    if 'tsv' == file_format:
        raw_data['Region'] = raw_data[raw_data.columns[0]].apply(lambda x: x.split(',')[-1])
    else:
        raw_data = raw_data.rename(columns={'country': 'Region'})
    
    # Filter the DataFrame where the Region is 'AL' or 'PT'
    df_sample = raw_data[(raw_data['Region'] == 'AL') | (raw_data['Region'] == 'PT')]

    if 'tsv' == file_format:
        df_sample = df_sample.drop(columns=['Region'])
        
        df_sample.to_csv(os.path.join(get_base_directory(), 'tests/fixtures', input_filename), 
                     sep='\t', index=False)
    else:
        df_sample = df_sample.rename(columns={'Region': 'country'})
        json_data = df_sample.to_json(orient='records', lines=False, indent=4)
        
        # Save JSON inside a ZIP file
        input_json_filename = input_filename.split('.', 1)[0] + '.json'
        
        full_zip_path = os.path.join(get_base_directory(), 'tests/fixtures', input_filename)
                
        with zipfile.ZipFile(full_zip_path, 'w') as zip_file:
            zip_file.writestr(input_json_filename, json_data)

    return df_sample


def create_output_sample_data(data: pd.DataFrame, 
                              output_folder_path: str, 
                              output_filename:str,
                              file_format: str)-> None:
    """Cleans and saves the sampled data for testing purposes"""
    cleaning_strategy: BaseCleaningStrategy

    if file_format == 'json':
        cleaning_strategy = DefaultCleaningStrategy()
    elif file_format == 'tsv':
        cleaning_strategy = TSVCleaningStrategy()

    gen_regions  = Region.generate_regions_dynamically(data, file_format)
    
    region = getattr(gen_regions, 'AL', None)

    if region is None:
        raise ValueError("Region 'AL' not found in the generated enum.")
    
    # Initialize the cleaner with the selected strategy
    cleaner = DataCleaner(strategy=cleaning_strategy)
    
    cleaned_data = cleaner.clean_data(data, region.value)

    cleaned_data = cleaned_data.where(cleaned_data.notnull(), '<<NONE>>')

    save_data(cleaned_data, output_folder_path, output_filename)


if __name__ == "__main__":
    # For tsv data
    '''
    input_folder_path, input_filename = 'data', 'eu_life_expectancy_raw.tsv'
    input_tsv_data = create_input_sample_data(input_folder_path, input_filename, 'tsv')

    output_folder_path, output_filename = 'tests/fixtures', 'eu_life_expectancy_expected.csv'
    create_output_sample_data(input_tsv_data, output_folder_path, output_filename, 'tsv')
    '''
    # For json data
    input_folder_path, input_filename = 'data', 'eurostat_life_expect.zip'
    input_json_data = create_input_sample_data(input_folder_path, input_filename, 'json')

    output_folder_path, output_filename = 'tests/fixtures', 'eurostat_life_expect.csv'
    create_output_sample_data(input_json_data, output_folder_path, output_filename, 'json')