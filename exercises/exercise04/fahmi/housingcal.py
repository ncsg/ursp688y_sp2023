import pandas as pd
import os

def affordable_housing_proportion():
   os.getcwd()
   housing_projects = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Excercise04_Fahmi/affordable_housing.csv')
   housing_projects = housing_projects[housing_projects['STATUS_PUBLIC'].str.startswith(('Under Construction','Pipeline'))]
   housing_projects_filtered = housing_projects[['MAR_WARD','STATUS_PUBLIC','AFFORDABLE_UNITS_AT_0_30_AMI','AFFORDABLE_UNITS_AT_31_50_AMI','AFFORDABLE_UNITS_AT_51_60_AMI']]
   housing_projects_filtered['Total_Units'] = housing_projects_filtered['AFFORDABLE_UNITS_AT_0_30_AMI']+ housing_projects_filtered['AFFORDABLE_UNITS_AT_31_50_AMI']++housing_projects_filtered['AFFORDABLE_UNITS_AT_51_60_AMI']
   housing_projects_filtered_total = housing_projects_filtered.groupby('MAR_WARD')[['Total_Units']].sum()
   ward_pop = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Excercise04_Fahmi/wards_from_2022.csv')
   ward_pop_filtered = ward_pop[['NAME','POP100']]
   ward_pop_filtered
   housing_projects_with_pops = pd.merge(
     housing_projects_filtered_total,
     ward_pop_filtered[['NAME','POP100']],
     left_on='MAR_WARD',
     right_on='NAME')
   housing_projects_with_pops['Percentage'] = housing_projects_with_pops['Total_Units']/ housing_projects_with_pops['POP100']*100
   return housing_projects_with_pops