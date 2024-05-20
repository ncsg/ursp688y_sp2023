# Import everything needed:
import os
import pandas as pd
import geopandas as gpd

# Create the first dataframe for the public housing data:
def create_housing_df(housing_projects, year):
    # Read the (precleaned) housing spreadsheet:
    housing_spreadsheet = pd.read_csv(housing_projects)
    # Create a condensed dataframe with only the necessary columns:
    housing_df = housing_spreadsheet[['NHPDPropertyID', 'PropertyName', 'PropertyAddress', 'City', 'Zip', 'CensusTract', 'Latitude', 'Longitude', 'PropertyStatus', 'TotalUnits', 'EarliestStartDate', 'LatestEndDate']].copy()
    # Convert the data for when each project's affordability contract started and ended(/ends) into datetime objects,
        # which makes it possible to filter projects by year:
    housing_df['EarliestStartDate'] = pd.to_datetime(housing_df['EarliestStartDate'])
    housing_df['EarliestStartYear'] = housing_df['EarliestStartDate'].dt.year
    housing_df['LatestEndDate'] = pd.to_datetime(housing_df['LatestEndDate'])
    housing_df['LatestEndYear'] = housing_df['LatestEndDate'].dt.year
    # Create a dataframe containing only the projects that had an active affordability contract for the year entered.
        # Sort that dataframe by start date and then reset the index:
    filtered_housing_df = housing_df[(housing_df['EarliestStartYear'] <= year) & (housing_df['LatestEndYear'] >= year)].sort_values('EarliestStartDate').reset_index()
    return filtered_housing_df

# Then make it into a geodataframe:
def create_housing_gdf(housing_projects, year):
    # Call the previous function:
    housing_df = create_housing_df(housing_projects, year)
    # Make a new column to house each project's geometry (or location):
    points = gpd.points_from_xy(housing_df['Longitude'], housing_df['Latitude'],  crs=4326)
    # Create the geodataframe with the desired coordinate system:
    gdf = gpd.GeoDataFrame(housing_df, geometry=points, crs=4326)
    return gdf

# Then map the geodataframe:
    # NOTE: Got help from this link: https://geopandas.org/en/stable/docs/user_guide/mapping.html
def map_housing_gdf(housing_projects, year, base):
    # Call the previous function:
    housing_gdf = create_housing_gdf(housing_projects, year)
    # This is the code that actually creates the map. Note that 'base' is a required argument; it will
        # later allow a layering effect with another map as the base/background.
    housing_map = housing_gdf.plot(ax=base, color='yellow', markersize=3)
    return housing_map

# NOTE: The above function won't work if you call it before setting a 'base'. That is done further down in this code.
# You can also set the base in the function itself if you want to use a different undermap (or if you want to test just this function).

# Import the census tract shapefile and standardize:
def fix_tract_data(raw_tract_data):
    # This code reads the inputted tract shapefile, converts its coordinate system, and then sorts the accompanying
        # attribute table by census tract and resets the index:
    tracts = gpd.read_file(raw_tract_data)
    tracts = tracts.to_crs('epsg:4326')
    fixed_tracts = tracts.sort_values('GISJOIN').reset_index()
    # The names of the census tract area field changed from year to year. The code below standardizes the field names so that
        # the code can be run regardless of year without needed to be changed:
    if raw_tract_data == 'PG_county_tracts_2010.shp':
        fixed_tracts = fixed_tracts.rename(columns={'Shape_area': 'SHAPE_AREA'})
    if  raw_tract_data == 'PG_county_tracts_2020.shp':
        fixed_tracts = fixed_tracts.rename(columns={'Shape_Area': 'SHAPE_AREA'})
    # Convert the listed area (which is in square meters) to square miles:
    fixed_tracts['Area_sq_miles'] = fixed_tracts['SHAPE_AREA']/2590000
    return fixed_tracts

# Next, join the Census tract data (which contains the geospatial information) and the
    # racial/demographic data (which contains the statistics of interest):
def join_race_to_tracts(raw_tract_data, raw_race_data):
    # Call the previous function:
    tract_df = fix_tract_data(raw_tract_data)
    # This sorts the demographic data by census tract, which -- because the two dataframes are now sorted in
        # the same way -- allows for an easy join:
    race_data = pd.read_csv(raw_race_data)
    race_data_df = race_data.sort_values('GISJOIN').reset_index()
    # Add the necessary columns from the demographic data to the Census tract data:
        # NOTE: Keep the column 'TRACTA' to ensure the joins are functioning correctly.
        # NOTE 2: 'Total_Hispanic' is included because I thought I might use it in my analysis, although I ended up not doing so.
    tract_df['CensusTract'] = race_data_df['TRACTA']
    tract_df['BlackNonHisp'] = race_data_df['Black']
    tract_df['TotalNonHisp'] = race_data_df['Total_Not_Hispanic']
    tract_df['TotalHisp'] = race_data_df['Total_Hispanic']
    tract_df['OverallTotal'] = race_data_df['Total']
    # Calculate the percent of the total population that is Black (or Hispanic) and add it to a new column:
    tract_df['PercentBlack'] = (tract_df['BlackNonHisp'] / tract_df['OverallTotal'])
    tract_df['PercentHisp'] = (tract_df['TotalHisp'] / tract_df['OverallTotal'])
    # Create a new dataframe that only contains the needed columns in a logical order:
    race_by_tract = tract_df[['GISJOIN', 'geometry', 'CensusTract', 'BlackNonHisp', 'TotalNonHisp', 'TotalHisp', 'OverallTotal', 'PercentBlack', 'PercentHisp', 'Area_sq_miles']].copy()
    return race_by_tract

# Then map this new geodataframe:
    # NOTE: Got help from this link for mapping: https://geopandas.org/en/stable/docs/user_guide/mapping.html
    # And from this link for a list of colors: https://matplotlib.org/stable/users/explain/colors/colormaps.html
def map_race_gdf(raw_tract_data, raw_race_data):
   # This code creates the map, sorts it by value/color, and adds a legend:
   race_map = join_race_to_tracts(raw_tract_data, raw_race_data).plot(column='PercentBlack', legend=True, cmap='Blues',
                           legend_kwds={'label': '% of Population that is Black'})
   return race_map

# This function joins the two geodataframes (the one for housing and the one for demographics):
def join_housing_to_tracts(housing_projects, year, raw_tract_data, raw_race_data):
    # Call two previous functions:
    housing_gdf = create_housing_gdf(housing_projects, year)
    tracts_with_race = join_race_to_tracts(raw_tract_data, raw_race_data)
    # Join the two geodataframes created by those functions:
    joined_gdf = housing_gdf.sjoin(tracts_with_race).sort_values('GISJOIN')
    # Create a new dataframe that only contains the needed columns in a logical order:
    final_gdf = joined_gdf[['NHPDPropertyID', 'PropertyName', 'TotalUnits', 'EarliestStartDate', 'LatestEndDate', 'EarliestStartYear',
       'LatestEndYear', 'CensusTract_right', 'BlackNonHisp', 'TotalNonHisp', 'TotalHisp',
       'OverallTotal', 'PercentBlack', 'PercentHisp', 'Area_sq_miles']]
    # Rename a column for clarity:
    final_gdf = final_gdf.rename(columns={'CensusTract_right': 'CensusTract'})
    return final_gdf

# This is the first part of the final product. It creates a map that overlays public housing projects on the demographic map.
    # NOTE: Got help from this link for mapping: https://geopandas.org/en/stable/docs/user_guide/mapping.html
def map_tracts(housing_projects, year, raw_tract_data, raw_race_data):
    # Call a previous fuction:
    housing_gdf = create_housing_gdf(housing_projects, year)
    # Set the base map to be the racial demographic data for the desired year:
        # NOTE: This makes the 'map_housing_gdf' function work, as it sets the 'base' parameter (as mentioned above).
    base = map_race_gdf(raw_tract_data, raw_race_data)
    # Create the final map:
    final_map = map_housing_gdf(housing_projects, year, base)
    return final_map

# Calculate the percent of the countywide population that is black so it can serve as a baseline later:
def countywide_percent_black(raw_tract_data, raw_race_data):
    # Call an earlier function that will produce a dataframe that allows this calculation:
    race_data = join_race_to_tracts(raw_tract_data, raw_race_data)
    # Calculate the statistic by taking the sums of two columns and dividing them:
    percent_black = (race_data['BlackNonHisp'].sum() / race_data['OverallTotal'].sum())
    return percent_black

# Calculate the countywide average public housing units per square mile so it can serve as a baseline later:
def countywide_units_per_sq_mile(housing_projects, year, raw_tract_data, raw_race_data):
    # Call two earlier functions that will produce dataframes that allow this calculation:
    housing_data = join_housing_to_tracts(housing_projects, year, raw_tract_data, raw_race_data)
    race_data = join_race_to_tracts(raw_tract_data, raw_race_data)
    # Calculate the statistic by taking the sums of two columns and dividing them:
    units_per_sq_mile = (housing_data['TotalUnits'].sum() / race_data['Area_sq_miles'].sum())
    return units_per_sq_mile

# This function produces a dataframe that contains data on every census tract that contains/contained
    # public housing for a given year:
def tracts_with_housing(housing_projects, year, raw_tract_data, raw_race_data):
    # Call an earlier function to produce the base dataframe:
    base_gdf = join_housing_to_tracts(housing_projects, year, raw_tract_data, raw_race_data)
    # Pull three statistics of interest from the base dataframe:
        # NOTE: 'percent_black' and 'area' use .mean() because groupby objects require some sort of function, and the mean of identical numbers produces the original number.
    units_per_tract = base_gdf.groupby('CensusTract')['TotalUnits'].sum()
    percent_black = base_gdf.groupby('CensusTract')['PercentBlack'].mean()
    area = base_gdf.groupby('CensusTract')['Area_sq_miles'].mean()
    # Combine these statistics into a new dataframe:
        # NOTE: Learned more about pd.concat here: https://stackoverflow.com/questions/28135436/concatenate-rows-of-two-dataframes-in-pandas
    df = pd.concat([units_per_tract, percent_black, area],
                  axis = 1)
    # Calculate the units per square mile for each census tract:
    df['Units_per_square_mile'] = df['TotalUnits']/df['Area_sq_miles']
    df = df.reset_index()
    return df

# This creates a version of the above dataframe that ONLY contains the tracts with an unequal distribution of public housing.
    # 'Unequal distribution' = above average black population and above average public housing unit density.
def filtered_tracts(housing_projects, year, raw_tract_data, raw_race_data):
    # Calculate the countywide averages for those two statistics using functions defined above:
    avg_percent_black = countywide_percent_black(raw_tract_data, raw_race_data)
    avg_units_per_sq_mile = countywide_units_per_sq_mile(housing_projects, year, raw_tract_data, raw_race_data)
    # Call the previous function that creates the unfiltered final dataframe:
    unfiltered_df = tracts_with_housing(housing_projects, year, raw_tract_data, raw_race_data)
    # Filter by only including census tracts from the original dataframe that meet a certain threshold (as defined above):
    filtered_df = unfiltered_df[(unfiltered_df['PercentBlack'] > avg_percent_black) & (unfiltered_df['Units_per_square_mile'] > avg_units_per_sq_mile)]
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df

# This function will highlight every row/tract in a datatable with an unequal distribution of public housing (as defined above).
    # It is generalized so that the thresholds and columns are chosen by the user. 
    # NOTE: Got help from here (and you, thanks again for office hours!): https://stackoverflow.com/questions/43596579/how-to-use-pandas-stylers-for-coloring-an-entire-row-based-on-a-given-column
def highlight_rows(row, threshold_a, threshold_b, column_a, column_b):
    # Only apply yellow background (or highlight) that exceed the threshold set:
    if (row.loc[column_a] > threshold_a) and (row.loc[column_b] > threshold_b):
        color = 'background-color: yellow'
    else:
        color = 'background-color: white'
    # Apply that highlight across the whole row -- not just a single cell.
    return [color] * len(row)

# This function sets the thresholds of the functions above and applies the highlight to a given dataframe:
def final_dataframe(housing_projects, year, raw_tract_data, raw_race_data):
    # Call an earlier function to create a dataframe that contains data on every census tract that contains/contained
        # public housing for a given year:
    final_df = tracts_with_housing(housing_projects, year, raw_tract_data, raw_race_data)
    # Calculate the countywide black population percentage and countywide average units per square mile:
    avg_percent_black = countywide_percent_black(raw_tract_data, raw_race_data)
    avg_units_per_sq_mile = countywide_units_per_sq_mile(housing_projects, year, raw_tract_data, raw_race_data)
    # Apply the highlight to that dataframe, set the thresholds, and set the columns:
    final_df = final_df.style.apply(highlight_rows, threshold_a = avg_percent_black, threshold_b = avg_units_per_sq_mile, column_a = 'PercentBlack', column_b = 'Units_per_square_mile', axis=1)
    return final_df

# Calculate the countywide average public housing units per square mile so it can serve as a baseline later:
def distribution_stats(housing_projects, year, raw_tract_data, raw_race_data):
    # Call two earlier functions that will produce dataframes that allow this calculation:
    total_tracts = len(join_race_to_tracts(raw_tract_data, raw_race_data).index)
    housing_tracts = len(tracts_with_housing(housing_projects, year, raw_tract_data, raw_race_data).index)
    unequal_tracts = len(filtered_tracts(housing_projects, year, raw_tract_data, raw_race_data).index)
    # Calculate the statistic by taking the sums of two columns and dividing them:
    # units_per_sq_mile = (housing_data['TotalUnits'].sum() / race_data['Area_sq_miles'].sum())
    housing_percentage = format((housing_tracts / total_tracts) * 100, '.2f')
    unequal_percentage = format((unequal_tracts / housing_tracts) * 100, '.2f')
    return f"In {year}, {housing_tracts} of {total_tracts} tracts (or {housing_percentage}%) contained public or publicly-funded housing units. Of these {housing_tracts} tracts, {unequal_tracts} (or {unequal_percentage}%) of them met the threshold for unequal distribution."
    