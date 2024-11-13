# pipeline.py

import os
import pandas as pd
import sqlite3
import requests


DATA_DIR = 'project/data'
DATABASE_PATH = os.path.join(DATA_DIR, 'cleaned_data.db')





def get_data(url, filename):
    """Downloads data from a URL to a local file."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        
    else:
        print(f"Download failed {filename}")


def cleaning_data(filename):
    
    df = pd.read_csv(filename)

    # write na into missing data
    df.fillna(0, inplace=True)  # Fill missing values with 0
    # Correct ages with number extraction
    df['Age'] = df['Age'].str.extract('(\d+)')
    df = df.drop(df[df['Gender'] == 0].index)
    
    return df


def save_to_database(df, table_name):
    
    with sqlite3.connect(DATABASE_PATH) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data saved to {table_name} table in {DATABASE_PATH}")


def main():
    # Define URL and filename
    url = "https://raw.githubusercontent.com/szabolcsfule/bear_attacks/master/bear_attacks.csv"  # Replace with actual data source URL
    raw_data_file = os.path.join(DATA_DIR, 'raw_data.csv')

   
    get_data(url, raw_data_file)

  
    cleaned_data = cleaning_data(raw_data_file)

    save_to_database(cleaned_data, "cleaned_data")


if __name__ == "__main__":
    main()
