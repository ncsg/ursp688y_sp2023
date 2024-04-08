# Import everything we need:
import os
import pandas as pd
import geopandas as gpd

# Import required data:
housing_projects = pd.read_csv('PG_county_public_housing.csv')
tracts = gpd.read_file('PGCountyCensusTracts.geojson')
race_data = pd.read_csv('PG_county_race_data.csv')

# Create the first dataframe for the public housing data:
def create_housing_df(housing_projects):
    housing_projects = housing_projects[['NHPDPropertyID', 'PropertyName', 'PropertyAddress', 'City', 'Zip', 'CensusTract', 'Latitude', 'Longitude', 'PropertyStatus', 'TotalUnits']]
    return housing_projects

# Then allow the user to filter by project status (active, inactive, inconclusive, or all):
def filter_by_status(status):
    # This makes it so that the entry is case insensitive:
    status = status.title()
    if status == 'Active' or status == 'Inconclusive' or status=='Inactive':
        housing_df = create_housing_df(housing_projects)
        # This extra step is what does the filtering, which is why it's not included in the 'all' option below:
        housing_df = housing_df.loc[housing_df['PropertyStatus'] == status]
    elif status == 'All':
        housing_df = create_housing_df(housing_projects)
    else:
        # If the entered argument is invalid (AKA not previously listed), the function will return the following error message:
        housing_df = "Please input 'Active', 'Inactive', 'Inconclusive', or 'All' for a valid result. Don't forget the quotation marks!"
    return housing_df

# Then make that filtered dataframe into a geodataframe:
def create_housing_gdf(status):
    # This makes it so that the entry is case insensitive:
    status = status.title()
    housing_df = filter_by_status(status)
    if status == 'Active' or status == 'Inconclusive' or status=='Inactive' or status=='All':
        # Convert longitude and latitude into sets of usable point data:
        points = gpd.points_from_xy(housing_df['Longitude'], housing_df['Latitude'],  crs=4326)
        # Create the geodataframe:
        gdf = gpd.GeoDataFrame(housing_df, geometry=points, crs=4326)
    else:
        # This code makes it so that invalid arguments will return the same error message as before:
        gdf = housing_df
    return gdf

# Then map the geodataframe:
    # NOTE: Got help from this link: https://geopandas.org/en/stable/docs/user_guide/mapping.html
def map_housing_gdf(status, base):
    # This makes it so that the entry is case insensitive:
    status = status.title()
    housing_gdf = create_housing_gdf(status)
    if status == 'Active' or status == 'Inconclusive' or status=='Inactive' or status=='All':
        # This is the code that actually creates the map. Note that I included 'base' as an argument to use
            # it here, as that will allow a layering effect later with another map as the base/background.
        map = housing_gdf.plot(ax=base, color='black', markersize=3)
    else:
        # This code makes it so that invalid arguments will return the same error message as before:
        map = housing_gdf
    return map

# Next, join the Census tract data (which contains the geospatial information) and the 
    # racial/demographic data (which contains the statistics):
def join_race_to_tracts():
    # The first row in the Census tract data contains data for the whole county; this line gets rid of it
        # and then sorts the values by geoid.
    tract_df = tracts.drop([0], axis=0).reset_index().sort_values('geoid')
    # This sorts the demographic data by census tract, which -- because the two dataframes are now sorted in
        # the same way -- allows for an easy join:
    race_data_df = race_data.sort_values('CensusTract')
    # Add the necessary columns from the demographic data to the Census tract data:
    tract_df['PercentBlack'] = race_data_df['PercentBlack']
    tract_df['CensusTract'] = race_data_df['CensusTract']
    race_by_tract = tract_df
    return race_by_tract

# Then map this new geodataframe:
    # NOTE: Got help from this link for mapping: https://geopandas.org/en/stable/docs/user_guide/mapping.html
    # And from this link for a list of colors: https://matplotlib.org/stable/users/explain/colors/colormaps.html
def map_race_gdf():
   # This code creates the map, sorts it by value/color, and adds a legend:
   map = join_race_to_tracts().plot(column='PercentBlack', legend=True, cmap='coolwarm',
                           legend_kwds={'label': '% of Population that is Black'})
   return map

# This function joins the two geodataframes (the one for housing and the one for demographics):
def join_housing_to_tracts(status):
    # This makes it so that the entry is case insensitive:
    status = status.title()
    housing_gdf = create_housing_gdf(status)
    if status == 'Active' or status == 'Inconclusive' or status=='Inactive' or status=='All':
        tracts_with_race = join_race_to_tracts()
        # The actual joining:
        joined_gdf = housing_gdf.sjoin(tracts_with_race)
    else:
        # This code makes it so that invalid arguments will return the same error message as before:
        joined_gdf = housing_gdf
    return joined_gdf

# Next, join the Census tract data (which contains the geospatial information) and the 
    # racial/demographic data (which contains the statistics):
def join_race_to_tracts():
    # The first row in the Census tract data contains data for the whole county; this line gets rid of it
        # and then sorts the values by geoid.
    tract_df = tracts.drop([0], axis=0).reset_index().sort_values('geoid')
    # This sorts the demographic data by census tract, which -- because the two dataframes are now sorted in
        # the same way -- allows for an easy join:
    race_data_df = race_data.sort_values('CensusTract')
    # Add the necessary columns from the demographic data to the Census tract data:
    tract_df['PercentBlack'] = race_data_df['PercentBlack']
    tract_df['CensusTract'] = race_data_df['CensusTract']
    race_by_tract = tract_df
    return race_by_tract

# Then map this new geodataframe:
    # NOTE: Got help from this link for mapping: https://geopandas.org/en/stable/docs/user_guide/mapping.html
    # And from this link for a list of colors: https://matplotlib.org/stable/users/explain/colors/colormaps.html
def map_race_gdf():
   # This code creates the map, sorts it by value/color, and adds a legend:
   map = join_race_to_tracts().plot(column='PercentBlack', legend=True, cmap='coolwarm',
                           legend_kwds={'label': '% of Population that is Black'})
   return map

# This function joins the two geodataframes (the one for housing and the one for demographics):
def join_housing_to_tracts(status):
    # This makes it so that the entry is case insensitive:
    status = status.title()
    housing_gdf = create_housing_gdf(status)
    if status == 'Active' or status == 'Inconclusive' or status=='Inactive' or status=='All':
        tracts_with_race = join_race_to_tracts()
        # The actual joining:
        joined_gdf = housing_gdf.sjoin(tracts_with_race)
    else:
        # This code makes it so that invalid arguments will return the same error message as before:
        joined_gdf = housing_gdf
    return joined_gdf

# This is the first part of the final product. It creates a map that overlays public housing projects on the demographic map.    
    # NOTE: Got help from this link for mapping: https://geopandas.org/en/stable/docs/user_guide/mapping.html
def map_tracts(status):
    # This makes it so that the entry is case insensitive:
    status = status.title()
    housing_gdf = create_housing_gdf(status)
    if status == 'Active' or status == 'Inconclusive' or status=='Inactive' or status=='All':
        # Set the demographic/census tract map as the lower layer, or base:
        base = map_race_gdf()
        # Create the final map with both layers:
        map = map_housing_gdf(status, base)
    else:
        # This code makes it so that invalid arguments will return the same error message as before:
        map = housing_gdf
    return map

# This is the second part of the final product. It allows you to input a Census tract in PG County
    # (as well as a status, like before) and returns the number of public housing units in that tract as well as
    # the percentage of that tract's population that is Black/African American.
def info_for_tract(tract, status):
    # This makes it so that the entry is case insensitive:
    status = status.title()
    all_tracts = join_housing_to_tracts(status)
    if status == 'Active' or status == 'Inconclusive' or status=='Inactive' or status=='All':
        # Calculate the sum of total public housing units in each Census tract:
        units = join_housing_to_tracts(status).groupby('CensusTract_right')['TotalUnits'].sum()
        # Pull the percentage of each Census tract's population that is Black/African American:
            #NOTE: I learned other methods for groupby() (AKA 'first()') at this link: https://pandas.pydata.org/docs/reference/groupby.html
        percent_AA = join_housing_to_tracts('all').groupby('CensusTract_right')['PercentBlack'].first()
        # This code only runs if the input for 'tract' is valid AND if that tract has at least one public housing unit:
        if tract in units:
            if status == 'Active' or status == 'Inconclusive' or status=='Inactive':
                # Pull the number of public housing units for the given tract:
                tract_units = units.loc[tract]
                # Make the 'status' input all lowercase to print a cleaner result:
                lowercase = status.lower()
                # Pull and format the percentage of the tract's population that is Black/African American:
                tract_AA = (percent_AA.loc[tract] * 100)
                result = (f"Tract {tract} has {tract_units} {lowercase} public housing unit(s). Its population is {tract_AA}% Black or African American.")
            elif status=='All':
                # This does the same thing, but the printed result is slightly different.
                tract_units = units.loc[tract]
                lowercase = status.lower()
                tract_AA = (percent_AA.loc[tract] * 100)
                result = (f"Tract {tract} has {tract_units} total public housing unit(s), whether active, inactive, or inconclusive. Its population is {tract_AA}% Black or African American.")
        else:
            # If the input is not a valid PG County tract, the chosen tract does not have any public housing
                # units, or the formatting is incorrect, it throws this error message:
            result = ("You have either (1) input an invalid Census tract or (2) chosen a Census tract with no public housing units under the set status. Please try again. It is important to note that all tract entries must have TWO DECIMAL PLACES (i.e. 8075.00) to be considered valid.")
    else:
        # This code makes it so that invalid arguments will return the same error message as before:
        result = all_tracts
    return result