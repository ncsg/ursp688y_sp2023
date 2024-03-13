import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

def analyze_bike_availability(api_url, local_json_path):
    # Fetching live data
    response = requests.get(api_url)
    data_live = response.json()
    df_live = pd.DataFrame(data_live['data']['bikes'])

    # Reading stored data
    with open(local_json_path) as json_data:
        data_stored = json.load(json_data)
    
    df_stored = pd.DataFrame(data_stored['data']['bikes'])
    
    # Processing timestamps and filtering available bikes
    df_live['timestamp'] = pd.to_datetime(df_live['timestamp'])
    df_live['hour'] = df_live['timestamp'].dt.hour
    available_bikes = df_live[(df_live['is_reserved'] == False) & (df_live['is_disabled'] == False)]
    
    # Calculating hourly unique counts
    hourly_unique_counts = available_bikes.groupby('hour')['bike_id'].nunique().reset_index(name='unique_bikes_count')
    
    # Plotting
    hourly_unique_counts = hourly_unique_counts.sort_values('hour')
    plt.figure(figsize=(12, 6))
    plt.plot(hourly_unique_counts['hour'], hourly_unique_counts['unique_bikes_count'], marker='o', linestyle='-', color='royalblue')
    plt.title('Hourly Distinct Count of Available Bikes')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Distinct Count of Available Bikes')
    plt.xticks(hourly_unique_counts['hour'])
    plt.grid(True)
    plt.show()
    
    # Finding max and min hours
    max_count_hour = hourly_unique_counts.loc[hourly_unique_counts['unique_bikes_count'].idxmax()]
    min_count_hour = hourly_unique_counts.loc[hourly_unique_counts['unique_bikes_count'].idxmin()]
    
    # Return the results
    max_min_df = pd.DataFrame([max_count_hour, min_count_hour], index=['Max', 'Min'])
    return max_min_df
# print(max_min_df)
