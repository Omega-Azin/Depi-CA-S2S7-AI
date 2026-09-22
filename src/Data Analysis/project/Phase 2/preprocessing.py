import pandas as pd
import numpy as np
import os

def clean_and_engineer_data(input_csv='201902-fordgobike-tripdata.csv', output_csv='cleaned_fordgobike_tripdata.csv'):
    """
    Part 2 - Preprocessing Pipeline:
    1. Clean data -> Fix missing values, remove outliers, standardize categories.
    2. Engineer features -> Trip duration in minutes, weekend flag, age groups, routes.
    """
    print(f"[*] Reading dataset from: {input_csv}...")
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Input file '{input_csv}' not found. Please ensure it is in the working directory.")

    df = pd.read_csv(input_csv)
    initial_shape = df.shape
    print(f"[*] Raw dataset shape: {initial_shape}")

    # 1. Clean Missing Values
    # Missing values in station IDs or user demographics are dropped to ensure valid dimensional relationships
    df.dropna(subset=['start_station_id', 'end_station_id', 'member_birth_year', 'member_gender'], inplace=True)
    print(f"[*] Dropped {initial_shape[0] - len(df)} rows with missing values.")

    # 2. Type Conversions
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df['start_station_id'] = df['start_station_id'].astype(int)
    df['end_station_id'] = df['end_station_id'].astype(int)
    df['bike_id'] = df['bike_id'].astype(int)
    df['member_birth_year'] = df['member_birth_year'].astype(int)

    # 3. Feature Engineering
    # A. Trip Duration in minutes
    df['duration_min'] = df['duration_sec'] / 60.0

    # B. User Age and Age Groups (dataset year is 2019)
    df['age'] = 2019 - df['member_birth_year']

    # Filter outliers: unrealistic age or trips shorter than 1 min or longer than 2 hours
    df = df[(df['age'] >= 10) & (df['age'] <= 85)]
    df = df[(df['duration_min'] >= 1.0) & (df['duration_min'] <= 120.0)]

    def categorize_age(age):
        if age < 25:
            return 'Young'
        elif 25 <= age <= 45:
            return 'Adult'
        else:
            return 'Senior'

    df['age_group'] = df['age'].apply(categorize_age)

    # C. Date and Temporal Features
    df['day_of_week'] = df['start_time'].dt.day_name()
    df['month'] = df['start_time'].dt.month_name()
    df['hour'] = df['start_time'].dt.hour
    df['start_date'] = df['start_time'].dt.strftime('%Y-%m-%d')
    df['weekend_flag'] = df['start_time'].dt.dayofweek.isin([5, 6]).astype(int)

    # D. Popular Route Feature
    df['route'] = df['start_station_name'] + ' -> ' + df['end_station_name']

    print(f"[*] Final clean dataset shape: {df.shape}")
    df.to_csv(output_csv, index=False)
    print(f"[+] Cleaned data saved successfully to: {output_csv}")
    return df

if __name__ == '__main__':
    clean_and_engineer_data()