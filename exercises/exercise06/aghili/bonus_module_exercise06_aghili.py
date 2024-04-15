# Import packages
import os
import json
import requests
import pandas as pd

def used_bikes(current):
    # Making a get request
    current = requests.get(
        'https://gbfs.lyft.com/gbfs/2.3/dca-cabi/en/free_bike_status.json')

    # Get JSON content
    current = current.json()

    # drill into the records for each bike
    current = current['data']['bikes']

    # convert to a dataframe
    current = pd.DataFrame(current)

    # Count the number of free bikes
    num = current['bike_id'].nunique()

    # Subtract the result from the total number
    # of bikes in the website
    used = 7000 - num

    # Print the answer
    answer = print(f'Currently {used} bikes are being used')
    return answer