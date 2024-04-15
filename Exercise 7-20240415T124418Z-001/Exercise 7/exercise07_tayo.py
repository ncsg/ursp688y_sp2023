import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from sklearn.cluster import KMeans
import contextily as ctx

def analyze_bus_parking(rapid_bus_path, parking_path):
    # Load the datasets
    rapid_bus_df = gpd.read_file('/content/drive/MyDrive/Exercise 7/Project Datascience/2030_Proposed_Rapid_Bus')
    bus_parking_df = gpd.read_file('/content/drive/MyDrive/Exercise 7/Project Datascience/Bus_Parking')

    # Perform proximity analysis
    proximity_analysis = gpd.sjoin(rapid_bus_df, bus_parking_df, how="left", op="intersects")
    proximity_analysis['distance_to_nearest'] = proximity_analysis.geometry.distance(bus_parking_df.unary_union)
    nearest_parking = proximity_analysis.groupby('SEGMENT_NA')['LOCATION'].first()
    rapid_bus_df_with_nearest_parking = rapid_bus_df.merge(nearest_parking, left_on='SEGMENT_NA', right_index=True)

    # Visualize proximity analysis
    fig, ax = plt.subplots(figsize=(10, 10))
    bus_parking_df.plot(ax=ax, color='blue', label='Bus Parking')
    rapid_bus_df.plot(ax=ax, color='red', label='Rapid Bus Segments')
    rapid_bus_df_with_nearest_parking.plot(ax=ax, color='green', markersize=50, label='Nearest Bus Parking')
    ctx.add_basemap(ax, zoom=12)
    plt.legend()
    plt.title('Proximity Analysis: Rapid Bus Segments and Nearest Bus Parking Locations')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    # Analyze parking spaces by attraction type
    plt.figure(figsize=(10, 8))
    bus_parking_df.groupby('ATTRACTION')['SPACES'].sum().sort_values().plot(kind='barh', color='skyblue')
    plt.title('Distribution of Available Parking Spaces by Attraction Type')
    plt.xlabel('Total Available Parking Spaces')
    plt.ylabel('Attraction Type')
    plt.grid(axis='x')
    plt.show()

    # Perform spatial clustering
    bus_parking_df['Latitude'] = bus_parking_df['geometry'].y
    bus_parking_df['Longitude'] = bus_parking_df['geometry'].x
    X = bus_parking_df[['Latitude', 'Longitude']]
    kmeans = KMeans(n_clusters=5, random_state=42)
    labels = kmeans.fit_predict(X)
    bus_parking_df['Cluster'] = labels

    # Visualize spatial clusters
    fig, ax = plt.subplots(figsize=(15, 8))
    bus_parking_df.plot(ax=ax, column='Cluster', cmap='viridis', legend=True)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Bus Parking Spatial Clusters')
    plt.grid(True)
    plt.show()


analyze_bus_parking('/content/drive/MyDrive/Exercise 7/Project Datascience/2030_Proposed_Rapid_Bus', '/content/drive/MyDrive/Exercise 7/Project Datascience/Bus_Parking')