import pandas as pd
import geopandas as gpd
!pip install osmnx
!pip install folium matplotlib mapclassify
import osmnx as ox
import networkx as nx
import folium
from shapely.geometry import Point
from sklearn.cluster import DBSCAN
from scipy.stats import gaussian_kde
import numpy as np

def analyze_school_accessibility(school_data_path, metro_data_path, place_name, threshold_distance, threshold_distance2, min_distance):
    # Pseudocode:
    # 1. Load school and metro station data from CSV files
    # 2. Create geometry columns for school and metro datasets
    # 3. Convert school and metro data to GeoDataFrames
    # 4. Load the road network graph for the specified place
    # 5. Project school and metro data to the same CRS as the road network
    # 6. Find the nearest node in the road network for each school and metro station
    # 7. Calculate the distance from each school to the nearest metro station
    # 8. Identify underserved schools based on distance thresholds
    # 9. Print statistics about underserved schools
    # 10. Create a map centered around the schools
    # 11. Add the road network, school markers, and metro station markers to the map
    # 12. Perform accessibility analysis to identify underserved schools
    #     - Project underserved schools to a suitable CRS for spatial analysis
    #     - Perform density analysis using kernel density estimation (KDE)
    #     - Identify areas with high density of underserved schools
    #     - Perform clustering analysis to group underserved schools
    #     - Identify the centroid of each cluster
    #     - Create a GeoDataFrame of potential metro station locations
    #     - Filter potential stations based on distance to existing metro stations
    # 13. Print the potential metro station locations
    # 14. Return the map
    from google.colab import drive
    drive.mount('/content/drive')
    school_data = pd.read_csv(school_data_path)
    metro_data = pd.read_csv(metro_data_path)

    if 'LATITUDE' in school_data.columns and 'LONGITUDE' in school_data.columns:
        school_data['geometry'] = gpd.points_from_xy(school_data['LONGITUDE'], school_data['LATITUDE'])
        print("Created geometry column for school dataset")
    else:
        print("Latitude and longitude columns not found in the school dataset")

    if 'X' in metro_data.columns and 'Y' in metro_data.columns:
        metro_data['geometry'] = gpd.points_from_xy(metro_data['X'], metro_data['Y'])
        print("Created geometry column for metro dataset")
    else:
        print("X and Y columns not found in the metro dataset")

    school_data = gpd.GeoDataFrame(school_data, geometry='geometry')
    metro_data = gpd.GeoDataFrame(metro_data, geometry='geometry')
    school_data.crs = 'EPSG:4326'
    metro_data.crs = 'EPSG:4326'
    graph = ox.graph_from_place(place_name, network_type='drive')
    schools_graph = school_data.to_crs(ox.utils_graph.graph_to_gdfs(graph, edges=False, node_geometry=True).crs)
    metro_graph = metro_data.to_crs(ox.utils_graph.graph_to_gdfs(graph, edges=False, node_geometry=True).crs)

    schools_graph['nearest_node'] = schools_graph.apply(lambda row: ox.distance.nearest_nodes(graph, row.geometry.x, row.geometry.y), axis=1)
    metro_graph['nearest_node'] = metro_graph.apply(lambda row: ox.distance.nearest_nodes(graph, row.geometry.x, row.geometry.y), axis=1)

    schools_graph['nearest_metro_distance'] = schools_graph.apply(lambda row: min(metro_graph.apply(lambda metro: nx.shortest_path_length(graph, source=row['nearest_node'], target=metro['nearest_node'], weight='length'), axis=1)), axis=1)
    schools_graph['nearest_metro_name'] = schools_graph.apply(lambda row: metro_graph.iloc[metro_graph.apply(lambda metro: nx.shortest_path_length(graph, source=row['nearest_node'], target=metro['nearest_node'], weight='length'), axis=1).idxmin()]['NAME'], axis=1)

    underserved_schools = schools_graph[schools_graph['nearest_metro_distance'] > threshold_distance]
    underserved_schools2 = schools_graph[schools_graph['nearest_metro_distance'] > threshold_distance2]

    total_schools = len(schools_graph)
    underserved_count = len(underserved_schools)
    underserved_count2 = len(underserved_schools2)
    underserved_percentage = (underserved_count / total_schools) * 100
    underserved_percentage2 = (underserved_count2 / total_schools) * 100

    print(f"Total schools: {total_schools}")
    print(f"Underserved schools (distance > {threshold_distance} meters): {underserved_count}")
    print(f"Underserved schools2 (distance > {threshold_distance2} meters): {underserved_count2}")
    print(f"Percentage of underserved schools: {underserved_percentage:.2f}%")
    print(f"Percentage of underserved schools2: {underserved_percentage2:.2f}%")
    print("\nUnderserved Schools:")
    print(underserved_schools[['NAME', 'nearest_metro_name', 'nearest_metro_distance']])
    print("\nUnderserved Schools2:")
    print(underserved_schools2[['NAME', 'nearest_metro_name', 'nearest_metro_distance']])
    !pip install folium matplotlib mapclassify
    map_center = schools_graph.unary_union.centroid
    m = folium.Map(location=[map_center.y, map_center.x], zoom_start=12)

    edges = ox.graph_to_gdfs(graph, nodes=False, fill_edge_geometry=True)
    edges.explore(m=m, color='gray')

    for idx, row in schools_graph.iterrows():
        if row['NAME'] in underserved_schools['NAME'].values:
            color = 'red'
        else:
            color = 'blue'
        folium.Marker(location=[row.geometry.y, row.geometry.x], popup=row['NAME'], icon=folium.Icon(color=color)).add_to(m)

    for idx, row in metro_graph.iterrows():
        folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, popup=row['NAME'], color='black', fill=True, fill_color='black').add_to(m)

    underserved_schools_projected = underserved_schools.to_crs(epsg=26918)

    x = underserved_schools_projected.geometry.x
    y = underserved_schools_projected.geometry.y

    xy = np.vstack([x, y])
    kde = gaussian_kde(xy, bw_method='scott')

    x_grid, y_grid = np.mgrid[x.min():x.max():100j, y.min():y.max():100j]
    positions = np.vstack([x_grid.ravel(), y_grid.ravel()])

    density = kde(positions)
    density = density.reshape(x_grid.shape)

    high_density_threshold = np.percentile(density, 75)
    high_density_areas = density > high_density_threshold

    coordinates = underserved_schools_projected.geometry.apply(lambda geom: [geom.x, geom.y]).tolist()
    dbscan = DBSCAN(eps=500, min_samples=3)
    cluster_labels = dbscan.fit_predict(coordinates)

    underserved_schools_projected['cluster'] = cluster_labels

    cluster_centroids = underserved_schools_projected.dissolve(by='cluster').centroid

    potential_stations = gpd.GeoDataFrame(geometry=cluster_centroids, crs=underserved_schools_projected.crs)
    potential_stations['name'] = 'Potential Metro Station'

    potential_stations['distance_to_nearest'] = potential_stations.geometry.apply(lambda geom: min(metro_graph.geometry.distance(geom)))

    potential_stations = potential_stations[potential_stations['distance_to_nearest'] > min_distance]

    print("Potential Metro Station Locations:")
    print(potential_stations[['name', 'geometry']])

    return m

school_data_path = '/content/drive/MyDrive/Folder python/DC_Public_Schools.csv'
metro_data_path = '/content/drive/MyDrive/Folder python/Metro_Stations_in_DC.csv'
place_name = "Washington, D.C., USA"
threshold_distance = 804.67
threshold_distance2 = 402.34
min_distance = 804.67

map_result = analyze_school_accessibility(school_data_path, metro_data_path, place_name, threshold_distance, threshold_distance2, min_distance)
map_result