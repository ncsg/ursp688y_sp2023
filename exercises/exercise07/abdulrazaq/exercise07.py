import os
import pandas as pd

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Set the working directory
os.chdir('/content/drive/MyDrive/exercise07_Abdulrazaq')
import geopandas as gpd
#whats in my directory?
os.listdir()
#Read shapefile
#data does not have shapefile format on the website, so i got csv, added layer then exported features from ArcGIs, hoping thats ecceptable
gdf = gpd.read_file('/content/drive/MyDrive/exercise07_Abdulrazaq/MTA')
gdf.head()
gdf.crs
gdf.plot()
crs = gdf.crs
crs
#trying sth different
import geopy.distance
# Define a function to calculate distance between two coordinates
def calculate_distance(coord1, coord2):
    return geopy.distance.geodesic(coord1, coord2).kilometers #adopted from chatgpt prompt:
    # (how to calculate distance between two points on the earth surface)
    #geodesic(coord1, coord2): This function calculates the geodesic distance between two points on the Earth's surface, given their latitude and longitude coordinates.
    #Geodesic distance is the shortest distance between two points on a curved surface, such as the Earth.
    # Calculate per pair distances between all subway stations
#for loop
#make a list to store average distances
average_distances = []
for i in range(len(gdf)):
    for j in range(i+1, len(gdf)):
        coord1 = (gdf.iloc[i]['Latitude'], gdf.iloc[i]['Longitude'])
        coord2 = (gdf.iloc[j]['Latitude'], gdf.iloc[j]['Longitude'])
        distance = calculate_distance(coord1, coord2)
        average_distances.append(distance)
print(average_distances)
# Compute the average distance between subway stations
average_distance = sum(average_distances) / len(average_distances)
print("Average distance between subway stations:", average_distance, "kilometers")

