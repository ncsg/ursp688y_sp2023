# Import libraries
import matplotlib.pyplot as plt
import pandas as pd
import os

#mount drive
from google.colab import drive
drive.mount('/content/drive')
os.chdir('/content/drive/MyDrive/ursp688y_shared_data')

#load and preview data
affordable_housing = pd.read_csv('affordable_housing.csv')
affordable_housing.head()

 #clean data
idx = affordable_housing[affordable_housing['MAR_WARD'] == '1'].index[0]
affordable_housing.at[idx, 'MAR_WARD'] = 'Ward 1'

# Confirm consistency
ward_counts = affordable_housing['MAR_WARD'].value_counts()
ward_counts

# referernce relevant columns for plotting
income_levels = ['AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI', 'AFFORDABLE_UNITS_AT_51_60_AMI', 'AFFORDABLE_UNITS_AT_61_80_AMI', 'AFFORDABLE_UNITS_AT_81_AMI']
income_levels

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#New figure
fig = plt.figure()

# Set the style of the plot
sns.set(style="whitegrid")


def plot_affordable_housing_by_status(affordable_housing, status):
     # Filter the data based on the provided project status
    filtered_data = affordable_housing[affordable_housing['STATUS_PUBLIC'] == status]

    # Grouping the data by income levels and sum the affordable units for each income level
    income_groups = ['AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI',
                     'AFFORDABLE_UNITS_AT_51_60_AMI', 'AFFORDABLE_UNITS_AT_61_80_AMI',
                     'AFFORDABLE_UNITS_AT_81_AMI']
  
    grouped_data = filtered_data.groupby('MAR_WARD')[income_groups].sum()
    # Plotting the grouped bar chart
    ax = grouped_data.plot(kind='bar', stacked=True, figsize=(10, 6))
    ax.set_xlabel('') #setting x axis to an empty string
    ax.set_ylabel('Number of Affordable Housing Units')
    ax.grid(False)
    ax.set_title('')
    plt.xticks(rotation=45)
    plt.legend(title='Income Level')
    plt.tight_layout()

    sns.despine()
    plt.show()
        

    #VISUALIZING D.C.'s  AFFORDABLE HOUSING (TODAY)
plot_affordable_housing_by_status(affordable_housing, 'Under Construction')

