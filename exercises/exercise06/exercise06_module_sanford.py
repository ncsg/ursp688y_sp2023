# These first few lines import everything these functions need to run -- see notebook for further explanation.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')

# This turns off an annoying warning message that kept popping up.
    # I did look into its meaning, but since my calculations were still returning as expected, I just turned it off.
pd.set_option('mode.chained_assignment', None)

def create_dataframe(df):
    # Remove and/or rearrange columns:
        # NOTE: I also took out 'is_reserved' and 'is_disabled' after checking that none of the listed bikes were reserved or disabled.
    df = df[['name', 'timestamp']]
    # Add 'hour' and 'date' column.
        # NOTE: I found this method at https://stackoverflow.com/questions/16266019/python-pandas-group-datetime-column-into-hour-and-minute-aggregations
        # These lines were the ones returning the warning messages before I turned it off.
    df['hour'] = df['timestamp'].dt.hour
    df['date'] = df['timestamp'].dt.day
    return df

def clean_data(df):
    # Call the previous function:
    df = create_dataframe(df)
    # Filter dataframe so that only 24 hours worth of data are included:
    df_a = df.loc[(df['hour'] >= 16) & (df['date'] == 3)]
    df_b = df.loc[(df['hour'] <= 15) & (df['date'] == 4)]
    # Recombine two filtered dataframes into one:
    df = pd.concat([df_a, df_b])
    # Sort entries by timestamp:
    df = df.sort_values('timestamp')
    # Reset index: (I don't think this step was necessary, but the old index was driving me crazy)
        # NOTE: I found this method at https://stackoverflow.com/questions/20490274/how-to-reset-index-in-a-pandas-dataframe
    df = df.reset_index(drop=True)
    return df

def free_bikes(df):
    # Call the previous function:
    df = clean_data(df)
    # Group the data by hour and date, with a column that counts the unique 'name' entries within each hour:
        # NOTE: I found the .nunique() method here: https://stackoverflow.com/questions/45759966/counting-unique-values-in-a-column-in-pandas-dataframe-like-in-qlik
    free_bikes = df.groupby([df['hour'], df['date']]).name.nunique()
    # Sort by (1) date and (2) hour:
    free_bikes = pd.DataFrame(free_bikes).sort_values(['date', 'hour'])
    # Reset index again:
    free_bikes = free_bikes.reset_index(drop=False)
    return free_bikes

def plot_bikes(df):
    # Call the previous function:
    free_bike_df = free_bikes(df)
    # Create the bar plot:
        # NOTE: I made the x axis the index value instead of hour to keep the plot in the order I want.
    ax = sns.barplot(free_bike_df, x=free_bike_df.index, y='name')
    # Fix the y axis range:
    ax.set(ylim=(900, 1000))
    # Add the hour values as x labels:
        # NOTE: Found this method here: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_xticks.html
    ax.set_xticks(free_bike_df.index, free_bike_df.hour)
        # Get rid of / edit the axis labels:
    ax.set(
        xlabel='Hour',
        ylabel=None)
    # Get rid of the box around it:
    sns.despine()
    # Give the plot a descriptive (if long) title:
    plt.title('Number of unique bikes available per hour, from 16:00 on 3/3/24 to 15:59 on 3/4/24')
    # Learned how to label bar values here: https://stackoverflow.com/questions/28931224/how-to-add-value-labels-on-a-bar-chart
    ax.bar_label(ax.containers[0], label_type='edge', fontsize=7)
    ax.margins(y=0.1)
    # Make sure that only the plot is returned, not the accompanying text:
    ax = plt.show(ax)
    return ax