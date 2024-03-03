import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def join_data(df_affordable_housing, df_ward_populations):
    # Ensure 'MAR_WARD' is converted to a numeric type
    df_affordable_housing['MAR_WARD'] = pd.to_numeric(df_affordable_housing['MAR_WARD'], errors='coerce')

    # Merge dataframes on 'MAR_WARD' and 'POP100' using right join
    df_combined = pd.merge(df_affordable_housing, df_ward_populations, how='right', left_on=['MAR_WARD'], right_on=['POP100'])

    return df_combined

def calculate_disproportion(df):
    df['housing_units_per_capita'] = df['TOTAL_AFFORDABLE_UNITS'] / df['POP100']
    return df

def process_data(affordable_housing_path, ward_populations_path):
    # Load data
    df_affordable_housing = load_data(affordable_housing_path)
    df_ward_populations = load_data(ward_populations_path)

    # Join data
    df_combined = join_data(df_affordable_housing, df_ward_populations)

    # Calculate disproportion
    df_result = calculate_disproportion(df_combined)

    return df_result

def main():
    # Specify file paths
    affordable_housing_path = '/content/drive/MyDrive/Colab Notebooks/Walker/Affordable_Housing_Data.csv'
    ward_populations_path = '/content/drive/MyDrive/Colab Notebooks/Walker/Wards_from_2022.csv'

    # Process data
    df_result = process_data(affordable_housing_path, ward_populations_path)

    # Display or analyze the results
    print(df_result)

    # Calculate and display wards with highest housing_units_per_capita
    high_disproportion = df_result.nlargest(8, 'housing_units_per_capita', 'all')
    print("Wards with highest housing_units_per_capita:")
    print(high_disproportion[['MAR_WARD', 'housing_units_per_capita']])

    # Calculate and display wards with lowest housing_units_per_capita
    low_disproportion = df_result.nsmallest(8, 'housing_units_per_capita', 'all')
    print("Wards with lowest housing_units_per_capita:")
    print(low_disproportion[['MAR_WARD', 'housing_units_per_capita']])

if __name__ == "__main__":
    main()