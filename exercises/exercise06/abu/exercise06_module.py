
def get_hourly_counts(df):

    # Set the working directory
    os.chdir('/content/drive/MyDrive/Exercises_Data_Science_John/ncsg ursp688y_sp2024 main exercises-exercise06')
     # Import module
    import exercise06
    # Making a get request
    response = requests.get('https://gbfs.lyft.com/gbfs/1.1/dca-cabi/en/free_bike_status.json')# Get JSON content
    data = response.json()
    # Inspect the contents
    data.keys()
    # Make a dataframe out of data for available bikes
    df = pd.DataFrame(data['data']['bikes'])
    # open a single stored json
    with open('cabi_data/cabi_bike_status_2024-03-03_13-11-54.json') as json_data: # Notice how I added 'cabi_data/' to the front of the path to get into that subdirectory where the jsons are stored?
        data = json.load(json_data)
        json_data.close()
        records = data['data']['bikes']
    # convert to a dataframe
    df = pd.DataFrame(records)
    # drop a column that we won't use, just to keep things clean
    df = df.drop(columns=['rental_uris'])
    df = exercise06.load_and_combine_free_bike_status_jsons_as_df('cabi_data')
    df
    import pandas as pd
    import matplotlib.pyplot as plt

    # Convert the 'timestamp' column to datetime dtype if it's not already in datetime format

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Extract the hours from the 'timestamp' column
    df['hour'] = df['timestamp'].dt.hour
    # Calculate hourly counts
    hourly_counts = df.groupby('hour').size().reset_index(name='count')
    return hourly_counts

    # the hour with least availabilty
    min_index = hourly_counts['count'].idxmin()
    min_index
    # the hour wth most availability
    max_index = hourly_counts['count'].idxmax()
    max_index

    import matplotlib.pyplot as plt
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_counts['hour'], hourly_counts['count'], marker='o', linestyle='-')
    #Giving the chart a heading
    plt.title('Counts of Occurrences by Hour')
    #Assign the hours to the x-axis
    plt.xlabel('Hour')
    #Assign coun to the Y-axis
    plt.ylabel('Count')
    #Set the x-axis ticks to show all 24 hours
    plt.xticks(range(24)) 
    #Introduce grid in the chart area 
    plt.grid(True)
    plt.show()
    