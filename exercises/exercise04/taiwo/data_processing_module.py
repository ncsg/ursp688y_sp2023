import os
import pandas as pd

def mount_google_drive():
    from google.colab import drive
    drive.mount('/content/drive')

def change_working_directory(wd_path):
    os.chdir(wd_path)
    print(f'Current working directory: {os.getcwd()}')

def load_data(housing_csv, demogs_csv):
    housing_projects = pd.read_csv(housing_csv)
    ward_demogs = pd.read_csv(demogs_csv)
    return housing_projects, ward_demogs

def preprocess_data(housing_projects, ward_demogs):
    housing_projects_with_pops = pd.merge(
        housing_projects,
        ward_demogs[['NAME', 'POP100', 'HU100']],
        left_on='MAR_WARD',
        right_on='NAME'
    )

    filtered_df = housing_projects_with_pops[
        (housing_projects_with_pops['STATUS_PUBLIC'] == 'Under Construction') |
        (housing_projects_with_pops['STATUS_PUBLIC'] == 'Pipeline')
    ]

    return filtered_df

def aggregate_and_calculate(df):
    df['total households with incomes up to 60% AMI'] = (
        df['AFFORDABLE_UNITS_AT_0_30_AMI'] +
        df['AFFORDABLE_UNITS_AT_31_50_AMI'] +
        df['AFFORDABLE_UNITS_AT_51_60_AMI']
    )
    
    grouped_df = df.groupby('MAR_WARD').agg({
        'total households with incomes up to 60% AMI': 'sum',
        'POP100': 'sum',
        'HU100': 'sum'
    }).reset_index()

    grouped_df['Units_Per_Population'] = grouped_df['total households with incomes up to 60% AMI'] / grouped_df['POP100']
    
    return grouped_df

def identify_wards_by_units(grouped_df):
    average_units_per_population = grouped_df['Units_Per_Population'].mean()

    wards_high_units = grouped_df[grouped_df['Units_Per_Population'] > average_units_per_population]
    wards_low_units = grouped_df[grouped_df['Units_Per_Population'] < average_units_per_population]
    
    return wards_high_units, wards_low_units

def main():
    # wd_path = '/content/drive/MyDrive/ursp688y_shared_data'
    # mount_google_drive()
    # change_working_directory(wd_path)

    housing_csv = 'affordable_housing.csv'
    demogs_csv = 'wards_from_2022.csv'

    housing_projects, ward_demogs = load_data(housing_csv, demogs_csv)
    filtered_df = preprocess_data(housing_projects, ward_demogs)
    grouped_df = aggregate_and_calculate(filtered_df)
    wards_high_units, wards_low_units = identify_wards_by_units(grouped_df)

    return wards_high_units, wards_low_units ### added return statement
    
    # print("Wards with high units:", wards_high_units)
    # print("Wards with low units:", wards_low_units)