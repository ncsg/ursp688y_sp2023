
# mount drive
from google.colab import drive
drive.mount('/content/drive')

# Import necessary libraries
import pandas as pd
import geopandas as gpd
import requests
import json
from shapely.geometry import Point
import folium
import matplotlib.pyplot as plt

# Loading and setting up Directry
wards_dc = gpd.read_file('/content/drive/MyDrive/Amanguah/URSP668Y_Data_Science/Amanguah_Exercise_folder/new_data/wards_dc')
ward7_boundary = wards_dc[wards_dc['WARD'] == 7]
# Load census tract data
census_tracts = gpd.read_file('/content/drive/MyDrive/Amanguah/URSP668Y_Data_Science/Amanguah_Exercise_folder/new_data/census_tracts')
# Load zoning designated data
zoning = gpd.read_file('/content/drive/MyDrive/Amanguah/URSP668Y_Data_Science/Amanguah_Exercise_folder/new_data/Zoning_Downtown_Designated_Streets')
# load street centerlines or characteristics data
street_centerlines = gpd.read_file('/content/drive/MyDrive/Amanguah/URSP668Y_Data_Science/Amanguah_Exercise_folder/new_data/Street_Centerlines_2013')
# Load bikeshare trip data
bikeshare_trip_data = pd.read_csv('/content/drive/MyDrive/Amanguah/URSP668Y_Data_Science/Amanguah_Exercise_folder/new_data/202312-capitalbikeshare-tripdata/202312-capitalbikeshare-tripdata.csv')
census_tracts.head(2)

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

# Answering Reseach Question one
# Store the EPSG code for UTM18
UTM18 = 26918

# Store the EPSG code for WGS84
WGS84 = 4326

# Reproject one of the GeoDataFrames to match the CRS of the other
bikeshare_station_gdf = bikeshare_station_gdf.to_crs(epsg=4326) 
# Perform spatial join
bikeshare_stations_in_ward7 = gpd.sjoin(bikeshare_station_gdf, ward7_boundary.to_crs(epsg=4326), how='inner', predicate='within')

# Re-project the geometries to UTM18 CRS
census_tracts = census_tracts.to_crs(epsg=UTM18)

# Calculate the centroid of each census tract
census_tracts['centroid'] = census_tracts.centroid

# Find the nearest bike share station for each census tract centroid
def find_nearest_station(row):
    nearest_station = min(bikeshare_stations_in_ward7.geometry, key=lambda g: g.distance(row.centroid))
    return nearest_station

census_tracts['nearest_station'] = census_tracts.apply(find_nearest_station, axis=1)

# Calculate the distance from each census tract centroid to the nearest bike share station
census_tracts['nearest_station_dist'] = census_tracts.apply(lambda row: row.centroid.distance(row.nearest_station), axis=1)
census_tracts['nearest_station_dist']
# Visualization of the Results
# Plot a histogram of nearest station distances
plt.hist(census_tracts['nearest_station_dist'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Distance to Nearest Bike Share Station')
plt.ylabel('Frequency')
plt.title('Distribution of Distance to Nearest Bike Share Station')
plt.grid(True)

plt.show()


# Answering Research Question two 
# Load the bike share station data
bikeshare_station_gdf = gpd.GeoDataFrame(bikeshare_station_gdf, geometry=gpd.points_from_xy(bikeshare_station_gdf['lon'], bikeshare_station_gdf['lat']))

# Reproject the geometries to a common coordinate system (UTM18)
bikeshare_station_gdf = bikeshare_station_gdf.to_crs(epsg=UTM18)
zoning = zoning.to_crs(epsg=UTM18)
street_centerlines = street_centerlines.to_crs(epsg=UTM18)

# Extract relevant station-level features
station_level_features = bikeshare_station_gdf[['station_id', 'name', 'capacity', 'lon', 'lat']]

# Merge the station level features data with the zoning data based on a common key
bikeshare_stations_with_zoning = gpd.sjoin(bikeshare_station_gdf, zoning, how='left', predicate='intersects')

# Convert 'started_at' and 'ended_at' columns to datetime objects
bikeshare_trip_data['started_at'] = pd.to_datetime(bikeshare_trip_data['started_at'])
bikeshare_trip_data['ended_at'] = pd.to_datetime(bikeshare_trip_data['ended_at'])

# Calculate trip duration in seconds
bikeshare_trip_data['trip_duration'] = (bikeshare_trip_data['ended_at'] - bikeshare_trip_data['started_at']).dt.total_seconds()

# Group the trip data by start station and calculate utilization metrics
station_utilization = bikeshare_trip_data.groupby('start_station_id')[['trip_duration']].agg(['count', 'mean'])
station_utilization.columns = ['total_trips', 'avg_trip_duration']
station_utilization = station_utilization.reset_index()
station_utilization.head(2)

# Re-project the 'bikeshare_stations_with_zoning' DataFrame to a common CRS
bikeshare_stations_with_zoning = bikeshare_stations_with_zoning.to_crs(epsg=3857)

# Merge the station-level features and utilization metrics
bikeshare_stations_with_data_combined_df = pd.concat([bikeshare_stations_with_zoning, station_utilization], axis=1)
bikeshare_stations_with_data_combined_df.head(2)

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

# Calculate correlation between station capacity and total trips
correlation = bikeshare_stations_with_data_combined_df[['capacity', 'total_trips']].corr().iloc[0, 1]
print(f'Correlation between station capacity and total trips: {correlation:.2f}')

# Create a map centered on Ward 7
ward7_centroid = bikeshare_stations_with_data_combined_df.geometry.unary_union.centroid

m = folium.Map(location=[ward7_centroid.y, ward7_centroid.x], zoom_start=12)

# Add the bike share stations to the map, colored by utilization
for _, row in bikeshare_stations_with_data_combined_df.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=row['name'],
        icon=folium.Icon(color='blue' if row['total_trips'] < 1000 else 'red', icon='bicycle')
    ).add_to(m)

# Add the zoning information to the map
folium.GeoJson(zoning, name='Zoning').add_to(m)

# Display the map
m

