
# Import necessary libraries
import os
from numpy.lib import twodim_base
import pandas as pd
import geopandas as gpd
import requests
import json
from shapely.geometry import Point
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from folium import GeoJson, Choropleth

# mount drive
from google.colab import drive
drive.mount('/content/drive')

os.chdir('/content/drive/MyDrive/Amanguah/URSP668Y_Data_Science/Amanguah_Exercise_folder/python project_exercise07')

wards_dc = gpd.read_file('wards_dc')
ward7_boundary = wards_dc[wards_dc['WARD'] == 7]
# Load census tract data
census_tracts = gpd.read_file('census_tracts')
# Load bikeshare trip data
bikeshare_trip_data = pd.read_csv('202312-capitalbikeshare-tripdata/202312-capitalbikeshare-tripdata.csv')
# Load zoning designated data
zoning = gpd.read_file('Zoning_Downtown_Designated_Streets')
# load point of interest data
poi_data = gpd.read_file('Points_of_Interest')
# load metro station data
metro_station_data = gpd.read_file('Metro_Stations_in_DC')
# load land use data
land_use_data = gpd.read_file('Existing_Land_Use')
#Attempt to simplify geometries
land_use_data['geometry'] = land_use_data.geometry.simplify(tolerance=0.01)  
#Check again if all geometries are valid after simplification
print(land_use_data.geometry.is_valid.all())
# Save the simplified data
land_use_data.to_file('simplified_data.shp')

# URL of the station information API endpoint
url = "https://gbfs.lyft.com/gbfs/2.3/dca-cabi/en/station_information.json"

# Send a GET request to the API endpoint
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the station data to a file
    with open("bike_stations.json", "w") as file:
        file.write(response.text)
    print("Station data downloaded successfully!")
else:
    print("Failed to download station data.")

# Load the JSON data
with open("bike_stations.json", "r") as file:
    data = json.load(file)
# Convert the data to a pandas DataFrame
bikeshare_station = pd.DataFrame(data["data"]["stations"])
# Convert the bikeshare_station DataFrame to a GeoDataFrame
bikeshare_station_gdf = gpd.GeoDataFrame(bikeshare_station, geometry=gpd.points_from_xy(bikeshare_station['lon'], bikeshare_station['lat']), crs='EPSG:4326')

# Store the EPSG code for UTM18
UTM18 = 26918

# Store the EPSG code for WGS84
WGS84 = 4326

bikeshare_station_gdf = bikeshare_station_gdf.to_crs(epsg=UTM18)
ward7_boundary = ward7_boundary.to_crs(epsg=UTM18)
census_tracts = census_tracts.to_crs(epsg=UTM18)

# Perform spatial join
bikeshare_stations_in_ward7 = gpd.sjoin(bikeshare_station_gdf, ward7_boundary, how='inner', predicate='within')

# Calculate the centroid of each census tract
census_tracts['centroid'] = census_tracts.centroid

# Find the nearest bike share station for each census tract centroid
def find_nearest_station(row):
    nearest_station = min(bikeshare_stations_in_ward7.geometry, key=lambda g: g.distance(row.centroid))
    return nearest_station

census_tracts['nearest_station'] = census_tracts.apply(find_nearest_station, axis=1)

# Calculate the distance from each census tract centroid to the nearest bike share station
census_tracts['nearest_station_dist'] = census_tracts.apply(lambda row: row.centroid.distance(row.nearest_station), axis=1)
#census_tracts['nearest_station_dist']

print(f"Mean distance: {census_tracts['nearest_station_dist'].mean():.2f} meters")
print(f"Median distance: {census_tracts['nearest_station_dist'].median():.2f} meters")
print(f"Maximum distance: {census_tracts['nearest_station_dist'].max():.2f} meters")

# Calculate the number of census tracts in Ward 7
num_census_tracts_in_ward7 = len(census_tracts==7)

# Calculate the number of bike share stations in Ward 7
num_bikeshare_stations_in_ward7 = len(bikeshare_stations_in_ward7)

# Define a walkability threshold distance (e.g., 400 meters)
walkability_threshold = 400

# Identify census tracts with limited bike share access
limited_access_tracts = census_tracts[census_tracts['nearest_station_dist'] > walkability_threshold]
print(f"Number of census tracts with limited bike share access: {len(limited_access_tracts)}")
print(f"Number of census tracts in Ward 7: {num_census_tracts_in_ward7}")
print(f"Number of bike share stations in Ward 7: {num_bikeshare_stations_in_ward7}")

## Visualization of question one ##

# Create Folium map
bikeshare_stations_in_ward7 = bikeshare_stations_in_ward7.to_crs(WGS84)
census_tracts = census_tracts.to_crs(WGS84)

# Create Folium map
bikeshare_stations_in_ward7 = bikeshare_stations_in_ward7.to_crs(WGS84)
census_tracts = census_tracts.to_crs(WGS84)

# Create a map centered on Ward 7
ward7_centroid = census_tracts.geometry.unary_union.centroid
m = folium.Map(location=[38.88, -76.95], zoom_start=12)

# Add ward7_boundary to the map
folium.GeoJson(ward7_boundary).add_to(m)

# Add the census tract boundaries to the map
folium.GeoJson(census_tracts, name='census_tracts').add_to(m)

# Add bike share stations to the map with popups
marker_cluster = MarkerCluster().add_to(m)
for idx, row in bikeshare_stations_in_ward7.iterrows():
    popup_text = f"Bike Share Station: {row['name']}"
    folium.Marker(
        [row.geometry.y, row.geometry.x],
        popup=popup_text
    ).add_to(marker_cluster)

# Add census tracts to the map, highlighting limited access tracts
folium.Choropleth(
    geo_data=census_tracts.__geo_interface__,
    name='Accessibility',
    data=census_tracts,
    columns=['NAME', 'nearest_station_dist'],
    key_on='feature.properties.NAME',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name='Distance to Nearest Bike Share Station (meters)'
).add_to(m)

# Display map
m

## Answering and Visualizing Question two ##

bikeshare_station_gdf = gpd.GeoDataFrame(
    bikeshare_station_gdf,
    geometry=gpd.points_from_xy(bikeshare_station_gdf['lon'], bikeshare_station_gdf['lat']),
    crs=WGS84)

# Reproject the geometries to a common coordinate system (UTM18)
bikeshare_station_gdf = bikeshare_station_gdf.to_crs(epsg=UTM18)
zoning = zoning.to_crs(epsg=UTM18)
land_use_data = land_use_data.to_crs(epsg=UTM18)
metro_station_data = metro_station_data.to_crs(epsg=UTM18)
poi_data = poi_data.to_crs(epsg=UTM18)
ward7_boundary = ward7_boundary.to_crs(epsg=UTM18)


# Extract relevant station-level features
station_level_features = bikeshare_station_gdf[['station_id', 'name', 'capacity', 'lon', 'lat']]

# Filter land use data to Ward 7
# Apply a buffer operation to fix potential topological errors
land_use_data['geometry'] = land_use_data.geometry.buffer(0)
ward7_boundary['geometry'] = ward7_boundary.geometry.buffer(0)

# Filter land use data to Ward 7
land_use_data_ward7 = gpd.clip(land_use_data, ward7_boundary)

# Filter metro stations to those within Ward 7
metro_station_data_ward7 = gpd.clip(metro_station_data, ward7_boundary)

# Filter POI data to those within Ward 7
poi_data_ward7 = gpd.clip(poi_data, ward7_boundary)


# Extract relevant station-level features
station_level_features = bikeshare_station_gdf[['station_id', 'name', 'capacity', 'lon', 'lat']]

# Merge station-level features with zoning data
bikeshare_stations_with_zoning = gpd.sjoin(bikeshare_station_gdf, zoning, how='left', op='intersects')


# Convert 'started_at' and 'ended_at' columns to datetime objects
bikeshare_trip_data['started_at'] = pd.to_datetime(bikeshare_trip_data['started_at'])
bikeshare_trip_data['ended_at'] = pd.to_datetime(bikeshare_trip_data['ended_at'])

# Calculate trip duration in seconds
bikeshare_trip_data['trip_duration'] = (bikeshare_trip_data['ended_at'] - bikeshare_trip_data['started_at']).dt.total_seconds()

# Group trip data by start station and calculate utilization metrics
station_utilization = bikeshare_trip_data.groupby('start_station_id')[['trip_duration']].agg(['count', 'mean'])
station_utilization.columns = ['total_trips', 'avg_trip_duration']
station_utilization = station_utilization.reset_index()

# Merge station-level features and utilization metrics
bikeshare_stations_with_data_combined_df = pd.concat([bikeshare_stations_with_zoning, station_utilization], axis=1)

# Calculate correlation between station capacity and total trips
correlation = bikeshare_stations_with_data_combined_df[['capacity', 'total_trips']].corr().iloc[0, 1]
print(f'Correlation between station capacity and total trips: {correlation:.2f}')


# Calculate distance to nearest metro station
bikeshare_stations_with_data_combined_df['dist_to_metro'] = bikeshare_stations_with_data_combined_df.geometry.apply(lambda g: metro_station_data.geometry.distance(g).min())
#bikeshare_stations_with_data_combined_df['dist_to_metro']


# Calculate distance to nearest land use type
for land_use_type in land_use_data_ward7['DESCRIPTIO'].unique():
    if land_use_type is not None:
        land_use_data_ward7_subset = land_use_data_ward7[land_use_data_ward7['DESCRIPTIO'] == land_use_type]
        bikeshare_stations_with_data_combined_df[f'dist_to_{land_use_type.lower().replace(" ", "_")}'] = \
            bikeshare_stations_with_data_combined_df.geometry.apply(
                lambda g: land_use_data_ward7_subset.distance(g).min())
#bikeshare_stations_with_data_combined_df 


# Create a list to store all calculated distances
distances = []

# Calculate distance to nearest POI
for poi_type in poi_data_ward7['NAME'].dropna().unique():
    poi_data_ward7_subset = poi_data_ward7[poi_data_ward7['NAME'] == poi_type]
    col_name = f"dist_to_{poi_type.lower().replace(' ', '_')}"
    distances.append(bikeshare_stations_with_data_combined_df.geometry.apply(lambda g: poi_data_ward7_subset.distance(g).min()))

# Concatenate all distances to create a DataFrame
distance_df = pd.concat(distances, axis=1)

# Rename columns
distance_df.columns = [f"dist_to_{poi_type.lower().replace(' ', '_')}" for poi_type in poi_data_ward7['NAME'].dropna().unique()]

# Concatenate the calculated distances with the original DataFrame
bikeshare_stations_with_data_combined_df = pd.concat([bikeshare_stations_with_data_combined_df, distance_df], axis=1)
#bikeshare_stations_with_data_combined_df


# Define marker size based on station utilization
marker_size = bikeshare_stations_with_data_combined_df['total_trips'] / 100

# Create a bubble plot of station capacity vs. total trips
plt.scatter(bikeshare_stations_with_data_combined_df['capacity'],
            bikeshare_stations_with_data_combined_df['total_trips'],
            s=marker_size, alpha=0.5)

plt.xlabel('Station Capacity')
plt.ylabel('Total Trips')
plt.title('Station Capacity vs. Total Trips')

# Add a color bar legend for marker sizes
plt.colorbar(label='Station Utilization')

plt.grid(True)
plt.show()


# Create Folium map
m = folium.Map(location=[38.88, -76.95], zoom_start=12)

# Add ward7_boundary to the map
folium.GeoJson(ward7_boundary).add_to(m)

# Filter bike share stations within Ward 7
bikeshare_stations_ward7 = bikeshare_stations_with_data_combined_df[bikeshare_stations_with_data_combined_df.geometry.within(ward7_boundary.unary_union)]

# Add bike share stations to the map
marker_cluster = MarkerCluster().add_to(m)

# Add markers for distance to metro stations
for idx, row in bikeshare_stations_ward7.iterrows():
    if 'dist_to_metro' in row:
        folium.Marker(location=[row['lat'], row['lon']], 
                      popup=f"Distance to Metro: {row['dist_to_metro']:.2f} meters",
                      icon=folium.Icon(color='blue')).add_to(marker_cluster)

# Add markers for distance to POI
for col in bikeshare_stations_ward7.columns:
    if col.startswith('dist_to_poi_'):
        poi_type = col.replace('dist_to_poi_', '').replace('_', ' ').title()
        for idx, row in bikeshare_stations_ward7.iterrows():
            if not pd.isnull(row[col]):
                folium.Marker(location=[row['lat'], row['lon']], 
                              popup=f"Distance to {poi_type}: {row[col]:.2f} meters",
                              icon=folium.Icon(color='yellow')).add_to(marker_cluster)

import math

# Add markers for distance to land use types
for col in bikeshare_stations_ward7.columns:
    if col.startswith('dist_to_') and not col.startswith('dist_to_poi_') and not col.startswith('dist_to_metro'):
        land_use_type = col.replace('dist_to_', '').replace('_', ' ').title()
        for idx, row in bikeshare_stations_ward7.iterrows():
            if not pd.isna(row[col]):
                folium.Marker(location=[row['lat'], row['lon']], 
                              popup=f"Distance to {land_use_type}: {row[col]:.2f} meters",
                              icon=folium.Icon(color='red')).add_to(marker_cluster)


# Display the map
m
