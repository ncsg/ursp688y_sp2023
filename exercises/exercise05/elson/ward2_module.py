
#import modules
import os
import pandas as pd
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import xticks

def plot_affordable_units_ward2():
    # set directory
    wd_path = '/content/drive/MyDrive/Colab Notebooks/exercise 05'
    os.chdir(wd_path)
    pd.options.mode.chained_assignment = None

    # Get data
    housing_projects = pd.read_csv('affordable_housing.csv')

    # Data cleaning (assuming the logic remains the same)
    if housing_projects['MAR_WARD'].str.contains('1').any():
        idx = housing_projects[housing_projects['MAR_WARD'] == '1'].index[0]
        housing_projects.at[idx, 'MAR_WARD'] = 'Ward 1'

    # Filter for desired projects
    ward_2_housing_proj = housing_projects[(housing_projects["MAR_WARD"].isin(["Ward 2"]))]

    # Select and rename desired columns
    selected_columns = ward_2_housing_proj[['STATUS_PUBLIC'] + [col for col in ward_2_housing_proj.columns if col.startswith('AFFORDABLE_UNITS_AT')]]
    selected_columns.rename(columns={"STATUS_PUBLIC": "Project Status"}, inplace=True)
    selected_columns.rename(columns={"AFFORDABLE_UNITS_AT_0_30_AMI": "0-30 AMI"}, inplace=True)
    selected_columns.rename(columns={"AFFORDABLE_UNITS_AT_31_50_AMI": "31-50 AMI"}, inplace=True)
    selected_columns.rename(columns={"AFFORDABLE_UNITS_AT_51_60_AMI": "51-60 AMI"}, inplace=True)
    selected_columns.rename(columns={"AFFORDABLE_UNITS_AT_61_80_AMI": "61-80 AMI"}, inplace=True)
    selected_columns.rename(columns={"AFFORDABLE_UNITS_AT_81_AMI": "81 AMI"}, inplace=True)

    # Melt data to separate AMI categories into rows (assuming AMI categories are in separate columns)
    melted_data = selected_columns.melt(id_vars='Project Status', var_name='AMI Category', value_name='Units')

    # Sort by Project Status and AMI Category
    melted_data = melted_data.sort_values(by=['Project Status', 'AMI Category'])

    # Create the plot using seaborn barplot
    plot = sns.barplot(
        x='Project Status',
        y='Units',
        hue='AMI Category',
        data=melted_data
    )

    # Clean and customize the plot
    plot.set_title('Affordable Units by AMI in Ward 2')
    plot.set_xlabel('Project Status')
    plot.set_ylabel(' Affordable Units')
    plt.xticks(rotation=45)

    return plot

plot_affordable_units_ward2()
