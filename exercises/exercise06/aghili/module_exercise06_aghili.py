
# Import packages
import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define a function that draws a bar graph
# grouped by hour blocks of the last 24 hours
def bikes_used_last_24h(df):

    # Filter the DataFrame and select the name and timestamp columns
    df = pd.DataFrame(df)[['name', 'timestamp']]

    # Add data and hour columns based on the timestamp column
    # Add 1 to the hour colums so the blocks start from 1
    df['date'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour

    # Group the Dataframe by hour and date
    # and use the nunique function to count the unique bike names
    df = df.groupby([df['hour'], df['date']]).nunique()
    df = pd.DataFrame(df).sort_values(
        ['date', 'hour'], ascending=False).reset_index()

    # Create a string type column for x labels
    df['blocks'] = df.hour.astype(str)

    # Plot the bar graph
    bar_graph = sns.barplot(data=df, x=df.index ,y='name')

    # Set ylim (y axis limit) to enhance readablility
    bar_graph.set(xlabel='Hour blocks', ylabel=None, ylim=(850, 1050))

    # Customize visualization
    bar_graph.set_xticklabels(df.blocks)
    plt.xticks(rotation=90)
    sns.despine()
    bar_graph.bar_label(
        bar_graph.containers[0],
        fmt="{:.0f}",
        label_type='edge',
        padding=5,
        rotation=90)
    plt.title(
        'The number of bikes used within the last 24 hours (Descending)')
    bar_graph.margins(y=10)
    plt.show()
    return bar_graph