# These first few lines import everything these functions need to run -- see notebook for further explanation.

import pandas as pd
housing_projects = pd.read_csv('affordable_housing.csv')

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')

# First, fix the housing data:
def fix_housing_data(housing_projects):
    # Filter the spreadsheet to only keep the columns we want:
    housing_df = pd.DataFrame(housing_projects)[['MAR_WARD', 'STATUS_PUBLIC', 'TOTAL_AFFORDABLE_UNITS', 'AFFORDABLE_UNITS_AT_0_30_AMI']]
    # Fix the typo in the data:
        # NOTE: I tried to make it so that this line won't run if you've already fixed the data or if you're using a different dataset.
    if housing_df.at[220, 'MAR_WARD'] == '1':
        housing_df.at[220, 'MAR_WARD'] = 'Ward 1'
    # To make arguments case insensitive, replace every instance of 'Completed 2015 to Date' with 'Completed 2015 To Date'.
        # This is necessary because I use the .title() method later in this code, which makes the first letter of every word uppercase.
        # I found the .replace() method here: https://stackoverflow.com/questions/25698710/replace-all-occurrences-of-a-string-in-a-pandas-dataframe-python 
    housing_df = housing_df.replace({'Completed 2015 to Date': 'Completed 2015 To Date'}, regex=True)
    return housing_df

# Next, create a function so the calculations and plot only include the specified status:
def filter_by_status(status):
    # If a valid status is entered, filter the results by that status and then preform the proper calculations:
    if status == 'Pipeline' or status == 'Under Construction' or status == 'Completed 2015 To Date':
        # Call the first function:
        filtered_df = fix_housing_data(housing_projects)
        # Filter by the entered status and sum everything by ward:
        filtered_df = filtered_df.loc[filtered_df['STATUS_PUBLIC'] == status].groupby('MAR_WARD').sum(numeric_only=True)
        # Calculate the statistic of interest, which is the percentage of total affordable units that are aimed at households making 30% of the AMI or less:
        filtered_df['30_AMI_PERCENTAGE'] = (filtered_df['AFFORDABLE_UNITS_AT_0_30_AMI'] / filtered_df['TOTAL_AFFORDABLE_UNITS']) * 100
        # Sort the results based on this new statistic:
        filtered_df = filtered_df.sort_values('30_AMI_PERCENTAGE')
    # I created this 'elif' so that users can enter 'complete' or 'completed' instead of the entire 'completed 2015 to date'.
        # Everything else is basically the same as the prior 'if' statement.
    elif status == 'Complete' or status == 'Completed':
        filtered_df = fix_housing_data(housing_projects)
        filtered_df = filtered_df.loc[filtered_df['STATUS_PUBLIC'] == 'Completed 2015 To Date'].groupby('MAR_WARD').sum(numeric_only=True)
        filtered_df['30_AMI_PERCENTAGE'] = (filtered_df['AFFORDABLE_UNITS_AT_0_30_AMI'] / filtered_df['TOTAL_AFFORDABLE_UNITS']) * 100
        filtered_df = filtered_df.sort_values('30_AMI_PERCENTAGE')
    # This 'elif' makes it possible to return the percentage of 30% AMI affordable units in each ward without specifying status.
        # In my notebook's example, you can do this by changing the argument from 'pipeline' to 'all'.
    elif status == 'All':
        filtered_df = fix_housing_data(housing_projects).groupby('MAR_WARD').sum(numeric_only=True)
        filtered_df['30_AMI_PERCENTAGE'] = (filtered_df['AFFORDABLE_UNITS_AT_0_30_AMI'] / filtered_df['TOTAL_AFFORDABLE_UNITS']) * 100
        filtered_df = filtered_df.sort_values('30_AMI_PERCENTAGE')
    # If the entered argument is invalid (AKA not previously listed), the function will return the following error message:
    else:
        filtered_df = "Please input 'Pipeline', 'Under Construction', 'Completed 2015 To Date' (or 'Complete'/'Completed'), or 'All' for a valid result. Don't forget the quotation marks!"
    return filtered_df

def plot_30_AMI(status):
    # This makes it so that the entry is case insensitive -- you can put in 'pipeline', 'PIPELINE', 'Pipeline', 'PIpelINe', etc.
    status = status.title()
    # Call the previous function, which in turn calls the one before:
    final_df = filter_by_status(status)
    # This 'if' statement makes sure that a plot is only created if a valid status is entered:
    if status == 'Pipeline' or status == 'Under Construction' or status == 'Completed 2015 To Date' or status == 'Complete' or status == 'Completed' or status == 'All':
        # Create the bar plot:
        ax = sns.barplot(final_df, x='MAR_WARD', y='30_AMI_PERCENTAGE')
        # Get rid of the axis labels:
        ax.set(
            xlabel=None,
            ylabel=None)
        # Get rid of the box around it:
        sns.despine()
        # Give the plot a descriptive (if long) title:
        plt.title(f'Percentage of Total Affordable Units for 30% AMI or Less, {status}')
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