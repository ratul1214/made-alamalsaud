# pipeline.py


import os
import pandas as pd
import sqlite3
import requests

import shutil


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

def get_dataFordf2(url, filename):
    """Downloads data from a URL to a local file."""
    shutil.copy(url, filename)


def cleaning_data1(df):
    # write na into missing data

    df.drop(['Latitude', 'Longitude'], axis=1, inplace=True)
    df = df.dropna(axis=0, how='all')
    # Correct ages with number extraction
    df['Age'] = df['Age'].str.extract('(\d+)')
    df['Location'] = df['Location'].apply(lambda x: x.split(',')[-1])
    return df

def cleaning_data2(df):
    # write na into missing data
    df.drop(['Latitude', 'Longitude'], axis=1, inplace=True)
    df = df.dropna(axis=0, how='all')
    df['Location'] = df['Location'].apply(lambda x: x.split(',')[-1])
    df = df.dropna(subset=[' age'])
    df['age'] = df[' age'].astype(int)
    df['Location'] = df['Location'].str.replace('\xa0', '', regex=False)
    return df


def save_to_database(df, table_name):

    with sqlite3.connect(DATABASE_PATH) as conn:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data saved to {table_name} table in {DATABASE_PATH}")


def main():
    # Define URL and filename
    url = "https://raw.githubusercontent.com/szabolcsfule/bear_attacks/master/bear_attacks.csv"  # Replace with actual data source URL
    raw_data_file1 = os.path.join(DATA_DIR, 'raw_data1.csv')
    raw_data_file2 = os.path.join(DATA_DIR, 'raw_data2.csv')
    od.download("https://www.kaggle.com/datasets/stealthtechnologies/bear-attacks-north-america/data")
    get_data(url,raw_data_file1)
    get_dataFordf2('bear-attacks-north-america/data (3).csv', raw_data_file2)
    df = pd.read_csv(raw_data_file1)

    df2 = pd.read_csv('bear-attacks-north-america/data (3).csv')
    cleaned_data1 = cleaning_data1(df)
    cleaned_data2 = cleaning_data2(df2)

    save_to_database(cleaned_data1, "cleaned_data")
    save_to_database(cleaned_data2, "cleaned_data2")


if __name__ == "__main__":
    main()
