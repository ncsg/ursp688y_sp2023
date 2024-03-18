#Mount to google drive
from google.colab import drive
drive.mount('/content/drive')
# Import dependencies
import os
import pandas as pd

# Set working directory
wd_path = '/content/drive/MyDrive/Amanguah/URSP668Y_Data_Science/Amanguah_Exercise_folder'
df_affordable = pd.read_csv('affordable_housing.csv')

# Find its location in the dataframe
idx = df_affordable[df_affordable['MAR_WARD'] == '1'].index[0]
print(f'inconsistent ward label is at index {idx}')
df_affordable.at[220, 'MAR_WARD'] = 'Ward 1'
df_affordable.head(2)

# Write a function to visualize affordable units between 31 to 50 AMI by ward
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')

def plot_affordable_housing_statistic(df_affordable, status='all', figsize=(10, 6), color='skyblue', rotation=45, grid=True):
    if status == 'all':
        filtered_df_affordable = df_affordable
        status_label = 'All Statuses'
    else:
        filtered_df_affordable = df_affordable[df_affordable['STATUS_PUBLIC'] == status]
        status_label = status.capitalize()

    if filtered_df_affordable.empty:
        print(f"No {status_label} projects found.")
        return

    ward_groups = filtered_df_affordable.groupby('MAR_WARD')['AFFORDABLE_UNITS_AT_31_50_AMI'].sum()

    plt.figure(figsize=figsize)
    ward_groups.plot(kind='bar', color=color)
    plt.title(f'Affordable Units Between 31 to 50 by Ward ({status_label} Projects)')
    plt.xlabel('Ward')
    plt.ylabel('Affordable Units')
    plt.xticks(rotation=rotation)
    if grid:
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Visualizing the three affordable housing Units for each Status:
#df_affordable = pd.read_csv('affordable_housing.csv')
plot_affordable_housing_statistic(df_affordable, status='Completed 2015 to Date')
plot_affordable_housing_statistic(df_affordable, status='Under Construction')
plot_affordable_housing_statistic(df_affordable, status='Pipeline')

#Alternative Function
def visualize_categories_by_ward(df_affordable):


    # Group the data by WARD and STATUS, then count occurrences
    counts = df_affordable.groupby(['MAR_WARD', 'STATUS_PUBLIC']).size().unstack(fill_value=0)

    # Plot the stacked bar chart
    plt.figure(figsize=(12, 6))
    counts.plot(kind='bar', stacked=True, color=['skyblue', 'yellow', 'lightgreen'])
    plt.title('Stacked Bar Plot of Categories by Ward')
    plt.xlabel('Ward')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='STATUS')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

visualize_categories_by_ward(df_affordable)
