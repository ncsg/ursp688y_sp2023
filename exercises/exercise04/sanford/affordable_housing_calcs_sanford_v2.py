import pandas as pd

# Recreate (with some edits) the work from Exercise 3:

def fix_housing_data(housing_projects):
   
    housing_df = pd.DataFrame(housing_projects)[['OBJECTID', 'MAR_WARD', 'STATUS_PUBLIC', 'AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI', 'AFFORDABLE_UNITS_AT_51_60_AMI']]
    # Fix the typo in the data:
        # NOTE: I tried to make it so that this line won't run if you've already fixed the data or if you're using a different dataset.
    if housing_df.at[220, 'MAR_WARD'] == '1':
        housing_df.at[220, 'MAR_WARD'] = 'Ward 1'
    # Add a new column that contains the sum of all units available to households with incomes up to 60% AMI:
    housing_df['Total affordable units <= 60% AMI'] =  housing_df[['AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI', 'AFFORDABLE_UNITS_AT_51_60_AMI']].sum(axis=1)
    # Filter so (1) only projects in the pipeline or under construction are included, and
        # (2) only the 'MAR_WARD' and 'Total affordable units <= 60% AMI' columns remain:
    housing_df = housing_df[['MAR_WARD', 'Total affordable units <= 60% AMI']].loc[(housing_df['STATUS_PUBLIC'] == 'Pipeline') | (housing_df['STATUS_PUBLIC'] == 'Under Construction')]
    # (1) Rename a column for readability, (2) recreate the dataframe so it shows each Ward's
        # total affordable units, and then (3) sort that dataframe by Ward
    housing_df = housing_df.rename(columns={'MAR_WARD': 'Ward'}).groupby('Ward').sum().sort_values('Ward')
    return housing_df

# Fix demographic data to make everything easier to join:

def fix_demographic_data(ward_demographics):
    # Create the dataframe with only the columns we need:
    demographic_df = pd.DataFrame(ward_demographics)[['NAME','POP100','HU100']]
     # (1) Rename columns for readability and  (2) sort by Ward:
    demographic_df = demographic_df.rename(columns={'NAME': 'Ward', 'POP100': 'Population', 'HU100': 'Housing units'}).sort_values('Ward')
    return demographic_df
    
# Join everything into one table and complete the analysis:

def affordable_proportion(housing_projects, ward_demographics):
    # Call functions above:
    housing_data = fix_housing_data(housing_projects)
    demographic_data = fix_demographic_data(ward_demographics)
    # Join the two tables based on ward:
    housing_and_demographic = pd.merge(demographic_data, housing_data, left_on='Ward', right_on='Ward').sort_values('Ward')
    # Create two new columns -- one that shows the percentage of total units in each ward that are affordable, and
        # one that shows how many affordable units there are per 100 people in each ward:
    housing_and_demographic['Affordable proportion of total units (%)'] = (housing_and_demographic['Total affordable units <= 60% AMI'] / housing_and_demographic['Housing units']) * 100
    housing_and_demographic['Affordable units per 100 people'] = (housing_and_demographic['Total affordable units <= 60% AMI'] / housing_and_demographic['Population']) * 100
    return housing_and_demographic