import pandas as pd
import os

def housing_status():
   os.getcwd()
   housing_projects = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Excercise04_Fahmi/affordable_housing.csv')
   housing_projects = housing_projects[housing_projects['STATUS_PUBLIC'].str.startswith(('Under Construction','Pipeline'))]
   housing_projects_filtered = housing_projects[['MAR_WARD','STATUS_PUBLIC','AFFORDABLE_UNITS_AT_0_30_AMI','AFFORDABLE_UNITS_AT_31_50_AMI','AFFORDABLE_UNITS_AT_51_60_AMI']]
   housing_projects_filtered['Total_Units'] = housing_projects_filtered['AFFORDABLE_UNITS_AT_0_30_AMI']+ housing_projects_filtered['AFFORDABLE_UNITS_AT_31_50_AMI']++housing_projects_filtered['AFFORDABLE_UNITS_AT_51_60_AMI']
   housing_projects_filtered_total = housing_projects_filtered['Total_Units']
   return housing_projects_filtered