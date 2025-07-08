
from curses import raw
from typing import final
from numpy import save, test
import pandas as pd
import os 
from sklearn.model_selection import train_test_split
import logging

log_dir="log"
os.makedirs(log_dir, exist_ok=True)

#logging configuration
logger=logging.getLogger('data_ingestion')
logger.setLevel('DEBUG')

console_handler=logging.StreamHandler()  #console handler
console_handler.setLevel('DEBUG')


log_file_path=os.path.join(log_dir, 'data_ingestion.log')
file_handler=logging.FileHandler(log_file_path)  #file handler
file_handler.setLevel('DEBUG')

formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_data(data_url:str) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Parameters:
    data_url (str): The URL or path to the CSV file.
    
    Returns:
    pd.DataFrame: The loaded data as a DataFrame.
    """
    try:
        df=pd.read_csv(data_url)
        logger.info(f"Data loaded successfully from {data_url}")
        return df
    except Exception as e:
        logger.error(f"Error loading data from {data_url}: {e}")
        raise

def preprocess_data(df:pd.DataFrame)->pd.DataFrame:
    """
    Preprocess the data by dropping null values and duplicates.
    
    Parameters:
    df (pd.DataFrame): The DataFrame to preprocess.
    
    Returns:
    pd.DataFrame: The preprocessed DataFrame.
    """
    try:
        df.drop(columns = ['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace = True)
        df.rename(columns = {'v1': 'target', 'v2': 'text'}, inplace = True)
        logger.debug("Columns renamed successfully")
        return df
    except Exception as e:
        logger.error(f"Error preprocessing data: {e}")
        raise

def save_data(train_data:pd.DataFrame, test_data:pd.DataFrame, data_path:str):
    """
    Save the train and test data to the specified directory.
    
    Parameters:
    train_data (pd.DataFrame): The training data.
    test_data (pd.DataFrame): The testing data.
    output_dir (str): The directory to save the data.
    """
    try:
        raw_data_path=os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, 'train.csv'), index=False)
        test_data.to_csv(os.path.join(raw_data_path, 'test.csv'), index=False)
        logger.info(f"Data saved successfully to {raw_data_path}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise

def main():
    try:
        test_size=0.2
        data_path="https://raw.githubusercontent.com/vikashishere/Datasets/main/spam.csv"
        df=load_data(data_path)
        final_df=preprocess_data(df)
        train_data, test_data=train_test_split(final_df, test_size=test_size, random_state=42)
        save_data(train_data, test_data, data_path="./data")
        logger.info("Data ingestion completed successfully")
    except Exception as e:
        logger.error(f"Error in data ingestion pipeline: {e}")
        raise
if __name__ == "__main__":
    main()
