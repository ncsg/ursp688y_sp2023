import pandas as pd

# Define a function for all the operations and calculations
def housing_analysis(ex_4_path):
    
    # import numpy as np

    # Import the .csv files
    df = pd.read_csv('affordable_housing.csv')

    # Filter rows with units only in
    # Developement Pipeline or Under Construction
    df = df[df['STATUS_PUBLIC'] == ('Pipeline' or 'Under Construction')]

    # Add a column titled AFFORDABLE_UNITS_UP_TO_60_AMI whose values
    # are the total of units up to 60 AMI
    df['AFFORDABLE_UNITS_UP_TO_60_AMI'] = df[[
        'AFFORDABLE_UNITS_AT_0_30_AMI',
        'AFFORDABLE_UNITS_AT_31_50_AMI',
        'AFFORDABLE_UNITS_AT_51_60_AMI']].sum(axis=1)

    # Select relevant columns
    relevant_cols = ['MAR_WARD',
        'STATUS_PUBLIC',
        'AFFORDABLE_UNITS_UP_TO_60_AMI',
        'TOTAL_AFFORDABLE_UNITS']

    df = df[relevant_cols]

    # Group by MAR_WARD
    grouped_df = df.groupby('MAR_WARD')[[
        'AFFORDABLE_UNITS_UP_TO_60_AMI',
        'TOTAL_AFFORDABLE_UNITS']].sum().reset_index()

    # Import the population file
    df_pop_2024 = pd.read_csv('wards_from_2024.csv')

    # Joining two tables with the keys
    # MAR_WARD in first and DP05_0001E in second
    housing_projects_with_pops = pd.merge(grouped_df, df_pop_2024,
        left_on='MAR_WARD', right_on='NAMELSAD')

    housing_projects_with_pops = pd.merge(
        grouped_df,
        df_pop_2024[['NAMELSAD','POP_2024']],
        left_on='MAR_WARD',
        right_on='NAMELSAD')

    # Adding a column whose values are the result of
    # devision between population and the
    housing_projects_with_pops['HOUSING_DISTRIBUTION_RATE'] = grouped_df[
        'TOTAL_AFFORDABLE_UNITS'] / df_pop_2024['POP_2024']

    # Saving the .csv file
    housing_projects_with_pops.to_csv(
        'affordable_housing_with_ward_pops.csv')

    # Loading the created file
    final_answer_full = pd.read_csv(
        'affordable_housing_with_ward_pops.csv')

    # Filtering selected columns
    final_select = final_answer_full.filter([
        'MAR_WARD',
        'AFFORDABLE_UNITS_UP_TO_60_AMI',
        'TOTAL_AFFORDABLE_UNITS',
        'POP_2024',
        'HOUSING_DISTRIBUTION_RATE'])

    # Coloring Min and Max
    color_grouped_df = final_select.style.highlight_max(
        color="green", axis=0).highlight_min(color="red", axis=0)

    # Returning the colored data
    return color_grouped_df