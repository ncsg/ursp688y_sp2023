import os
import pandas as pd
import json

def load_and_combine_free_bike_status_jsons_as_df(json_dir):
    """Loads multiple GBFS free_bike_status jsons into a single DataFrame with timestamps

    json_dir: path to folder where jsons are stored
    """
    # Initiate a list to store all my dataframes in
    dfs = []
    # Loop through files in the cabi_data directory (notice this is a path relative to my current working directory?)
    for file in os.listdir(json_dir):
        # Only move forward if the last five characters of the file name are .json
        if file[-5:] == '.json':
            # Load the json file
            file_path = os.path.join(json_dir, file) # This function intelligently combines parts of paths into a single string
            with open(file_path) as json_data:
                data = json.load(json_data)
                json_data.close()
            # Make bike records into a dataframe
            bikes_df = pd.DataFrame(data['data']['bikes'])
            # Get timestamp
            timestamp = data['last_updated']
            # Save timestamp as a column in the dataframe
            bikes_df['timestamp'] = timestamp
            # Store dataframe
            dfs.append(bikes_df)
    # Concatenate all the dataframes together into a single dataframe
    df = pd.concat(dfs)
    # Convert POSIX timestamp in UTC to datetime object
    # For reference: https://stackoverflow.com/questions/65948018/how-to-convert-unix-epoch-time-to-datetime-with-timezone-in-pandas
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
    # Then convert to US Eastern time
    df['timestamp'] = df['timestamp'].dt.tz_convert('US/Eastern')
    # Delete a column we don't need
    df = df.drop(columns=['rental_uris'])
    return df