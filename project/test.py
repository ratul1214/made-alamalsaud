import os
import pandas as pd
import sqlite3

from main import cleaning_data1, cleaning_data2, DATABASE_PATH


def test_cleaning_data1():
    sample_data = {
        'Latitude': [10, 20],
        'Longitude': [30, 40],
        'Age': ['25 years', '30 years'],
        'Location': ['City, Country', 'Town, Country'],
        'Date': ['January 2021', 'February 2022']
    }
    df = pd.DataFrame(sample_data)
    cleaned_df = cleaning_data1(df)

    assert 'Latitude' not in cleaned_df.columns
    assert 'Longitude' not in cleaned_df.columns
    assert cleaned_df['Age'].tolist() == ['25', '30']
    assert cleaned_df['Location'].tolist() == ['Country', 'Country']


def test_database():
    # Connect to the database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Check for tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert "cleaned_data" in tables
    assert "cleaned_data2" in tables

    # Check columns in cleaned_data table
    cursor.execute("PRAGMA table_info(cleaned_data);")
    cleaned_data_columns = [col[1] for col in cursor.fetchall()]
    expected_columns = ["Age", "Location", "Year", "Month"]
    for col in expected_columns:
        assert col in cleaned_data_columns

    # Check columns in cleaned_data2 table
    cursor.execute("PRAGMA table_info(cleaned_data2);")
    cleaned_data2_columns = [col[1] for col in cursor.fetchall()]
    expected_columns2 = ["age", "Location", "ParsedDate", "Month", "Year"]
    for col in expected_columns2:
        assert col in cleaned_data2_columns

    # Validate specific data values in cleaned_data
    cursor.execute("SELECT COUNT(*) FROM cleaned_data;")
    count_cleaned_data = cursor.fetchone()[0]
    assert count_cleaned_data > 0, "cleaned_data table should not be empty"

    cursor.execute("SELECT DISTINCT Year FROM cleaned_data;")
    years = [row[0] for row in cursor.fetchall()]
    assert all(isinstance(year, str) and len(year) == 4 for year in
               years), "Year column should contain valid years in string format"

    # Validate specific data values in cleaned_data2
    cursor.execute("SELECT COUNT(*) FROM cleaned_data2;")
    count_cleaned_data2 = cursor.fetchone()[0]
    assert count_cleaned_data2 > 0, "cleaned_data2 table should not be empty"

    cursor.execute("SELECT MIN(age), MAX(age) FROM cleaned_data2;")
    min_age, max_age = cursor.fetchone()
    assert min_age >= 0, "Age column should have non-negative values"
    assert max_age <= 120, "Age column should have realistic values"

    conn.close()
