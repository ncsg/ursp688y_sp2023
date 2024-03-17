# Connecting to my Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Import pandas and numpy
import pandas as pd
import numpy as np

# Import matplotlib and seaborn
import matplotlib.pyplot as plt
import seaborn as sns

housing_df = pd.read_csv('affordable_housing.csv')

# Defining a function based on an argument
# in the STATUS_PUBLIC
def housing_percentage(data):

    filtered_df = pd.DataFrame(housing_df)[['MAR_WARD', 'STATUS_PUBLIC', 'TOTAL_AFFORDABLE_UNITS', 'AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI']]

    # Define a condition to group the DataFrame
    # based on values in STATUS_PUBLIC
    if data == 'Pipeline' or data == 'Under Construction' or data == 'Completed 2015 to Date':

        filtered_df = filtered_df.loc[filtered_df['STATUS_PUBLIC'] == data].groupby('MAR_WARD').sum(numeric_only=True)

        # Write the operation to create the percentage column
        filtered_df['UP_TO_30_AMI_PERCENTAGE'] = filtered_df['AFFORDABLE_UNITS_AT_0_30_AMI'] / filtered_df['TOTAL_AFFORDABLE_UNITS'] * 100

        filtered_df = filtered_df.sort_values('UP_TO_30_AMI_PERCENTAGE')

    elif data == 'Total':

        filtered_df = filtered_df.groupby('MAR_WARD').sum(numeric_only=True)

        # Write the operation to create the percentage column
        filtered_df['UP_TO_30_AMI_PERCENTAGE'] = filtered_df['AFFORDABLE_UNITS_AT_0_30_AMI'] / filtered_df['TOTAL_AFFORDABLE_UNITS'] * 100
        filtered_df = filtered_df.sort_values('UP_TO_30_AMI_PERCENTAGE')


    # Write a statement in case the argument input was incorrect
    else:
        filtered_df == print("Please input 'Pipeline', 'Under Construction', 'Completed 2015 to Date', 'Total'")

    return filtered_df

    from pickle import NONE
def graph_up_to_30_ami(data):

    # Call the previous function, which in turn calls the one before:
    final_df = housing_percentage(data)
    # This 'if' statement makes sure that a plot is only created if a valid status is entered:
    if data == 'Pipeline' or data == 'Under Construction' or data == 'Completed 2015 to Date' or data == 'Total':
        # Create the bar graph:
        ax = sns.barplot(final_df, x='MAR_WARD', y='UP_TO_30_AMI_PERCENTAGE')
        # Get rid of the axis labels:
        ax.set(
            xlabel=None,
            ylabel=None)
        # Get rid of the box around it:
        sns.despine()
        # Give the plot a descriptive (if long) title:
        plt.title(f'Percentage of Total Affordable Units for 30% AMI or Less, {data}')
        # Learned how to label bar values here: https://stackoverflow.com/questions/28931224/how-to-add-value-labels-on-a-bar-chart
        # Learned how to limit significant figures here: https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
        ax.bar_label(ax.containers[0], fmt="{:.2f}", label_type='edge')
        ax.margins(y=0.1)
        # Make sure that only the plot is returned, not the accompanying text:
        ax = plt.show(ax)
    # If the entered argument is invalid, the function will return the same error message as before.
    else:
        ax = final_df
    return ax
