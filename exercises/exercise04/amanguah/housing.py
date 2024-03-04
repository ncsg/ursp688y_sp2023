#Mount to google drive
from google.colab import drive
drive.mount('/content/drive')

# Import dependencies
import os
os.getcwd()

# Set working directory
wd_path = '/content/drive/MyDrive/ursp688y_shared_data-20240224T193244Z-001 (2)/ursp688y_shared_data'
os.chdir(wd_path)

print(f'cwd: {os.getcwd()}')

os.path.isfile('affordable_housing.csv')

import pandas as pd

df = pd.read_csv('affordable_housing.csv')

# Filter the dataframe  for the project status under Pipeline and under construction
filtered_df = df[(df['STATUS_PUBLIC'] == 'Under Construction') | (df['STATUS_PUBLIC'] == 'Pipeline')]
filtered_df.head()

# To use groupby founction to group the filtered data for affordable units from 0-30%, 31-50%, and 51-60% in each ward
ward_units = filtered_df.groupby('MAR_WARD')['AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI', 'AFFORDABLE_UNITS_AT_51_60_AMI'].sum()
ward_units

# Aggregate the Total Affordable Units up to 60% for each of the wards
ward_units['Total_Affordable_Units_Up_To_60%_AMI'] = ward_units.sum(axis=1)
ward_units['Total_Affordable_Units_Up_To_60%_AMI']
ward_total = ward_units['Total_Affordable_Units_Up_To_60%_AMI']
ward_total

# find ward with most units
ward_most_units = ward_units['Total_Affordable_Units_Up_To_60%_AMI'].idxmax()
ward_most_units
# find ward with least units
ward_fewest_units = ward_units['Total_Affordable_Units_Up_To_60%_AMI'].idxmin()
ward_fewest_units

# Set ward working directory
abs_path = '/content/drive/MyDrive/ursp688y_shared_data-20240224T193244Z-001 (2)/ursp688y_shared_data/wards_from_2022.csv'
os.path.isfile(abs_path)
# create a dataframe for the word with population
df_ward = pd.read_csv('wards_from_2022.csv')
df_ward.head()

# Merge the Affordable housing units and the wards with population
df_with_pops = pd.merge(ward_total, df_ward, left_on='MAR_WARD', right_on='NAME')
#  Joining the two files together
df_with_pops = pd.merge(
    ward_total,
    df_ward[['NAME','POP100','HU100']],
    left_on='MAR_WARD',
    right_on='NAME')

df_with_pops

# Calculate the disproportionately largest and smallest housing ratio
df_with_pops['Affordable_Units_Ratio'] = df_with_pops['Total_Affordable_Units_Up_To_60%_AMI'] / df_with_pops['POP100']

df_with_pops

#Identify the ward with the largest Affordable_Units_Ratio
ward_with_largest_ratio = df_with_pops.loc[df_with_pops['Affordable_Units_Ratio'].idxmax(), 'NAME']
print("Ward with the largest Affordable_Units_Ratio:", ward_with_largest_ratio)

# Identify the ward with the smallest Affordable_Units_Ratio
ward_with_smallest_ratio = df_with_pops.loc[df_with_pops['Affordable_Units_Ratio'].idxmin(), 'NAME']
print("Ward with the smallest Affordable_Units_Ratio:", ward_with_smallest_ratio)










