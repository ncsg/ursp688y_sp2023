import pandas as pd

   
    drive.mount( '/content/drive')

    # Load affordable housing data
    affordable_housing_data = pd.read_csv('affordable_housing.csv')

    # Load ward population data
    ward_population_data = pd.read_csv('wards_from_2022.csv')

    return affordable_housing_data, ward_population_data

# Call the load_data() function and assign result to variables
affordable_housing_data, ward_population_data = load_data()

# Display the DataFrames - Housing first
affordable_housing_data.head()

#Display population data frame
ward_population_data.head()

# merging ward named "1" with actual "Ward 1"
idx = affordable_housing_data[affordable_housing_data['MAR_WARD'] == '1'].index[0]
affordable_housing_data.at[idx, 'MAR_WARD'] = 'Ward 1'

#Function to join population and housing csv data
def join_data(affordable_housing_data, ward_population_data):
    #the LABEL column in ward (pop) data and MAR_WARD column in housing data have the same information (Ward ID)
    # - manually checked. bad practice I Know!
    # Merge housing data with population data using the common factor on ward ID
    merged_data = pd.merge(affordable_housing_data, ward_population_data, left_on='MAR_WARD', right_on='LABEL')
    # Call the join_data function and assign the result to a variable
    merged_data = join_data(affordable_housing_data, ward_population_data)

# Now lets preview the columns
print(merged_data.columns.tolist())

#Now use a boolean mask to filter objects exckuding 'Completed 2015 to Date' - to get those that are still in progress
def filterTable(merged_data):
    under_construction = merged_data['STATUS_PUBLIC'] != 'Completed 2015 to Date'
    return under_construction

def getTotalUnitsUpTo60AMI(merged_data):
    return merged_data[['AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI', 'AFFORDABLE_UNITS_AT_51_60_AMI']].sum(axis=1)

# Sum units available up to 60 AMI
def adviceCityOfficials(merged_data):
    # Call a function to filter the  table and obtain a boolean mask indicating projects under construction
    under_construction = filterTable(merged_data)
    
    # Apply the boolean mask to the supplied table to filter the data and store the result in a new variable
    filtered_data = merged_data[under_construction]
    
    # Group the filtered data by 'MAR_WARD' and calculate the sum of 'Affordable Units Available Up To 60% AMI' for each group
    grouped_data = filtered_data.groupby(['MAR_WARD'])['Affordable Units Available Up To 60% AMI'].sum()
    
    # Return the grouped data, which represents the sum of affordable units available up to 60% AMI for projects under construction in each ward 
    return grouped_data

# Export merged data to a CSV file
 def merge_data():
    merge_data =  merged_data.to_csv("merged_data.csv", index=False)  # Specify index=False to exclude row numbers
    return merged_data

#Function to calculate and identify disproportionate units
def calculate_disproportionate_units(merged_data):
    # Calculate housing units per capita
    merged_data['housing_units_per_capita'] = merged_data['TOTAL_AFFORDABLE_UNITS'] / merged_data['POP100']

    # Calculate mean housing units per capita across all wards
    mean_units_per_capita = merged_data['housing_units_per_capita'].mean()

    # Calculate standard deviation of housing units per capita across all wards
    std_units_per_capita = merged_data['housing_units_per_capita'].std()

    # Define threshold for disproportionately large/small housing units per capita
    threshold = 1.5

    # Identify disproportionately large and small wards
    disproportionately_large = merged_data[merged_data['housing_units_per_capita'] > (mean_units_per_capita + threshold * std_units_per_capita)]
    disproportionately_small = merged_data[merged_data['housing_units_per_capita'] < (mean_units_per_capita - threshold * std_units_per_capita)]

    return disproportionately_large, disproportionately_small
# Call  main function
#Main function will call all other functions sequentially
def main():
    # Load data
    affordable_housing_data, ward_population_data = load_data()

    # Join data
    merged_data = join_data(affordable_housing_data, ward_population_data)

    # Calculate disproportionately large and small housing units
    disproportionately_large, disproportionately_small = calculate_disproportionate_units(merged_data)

   # Export disproportionately large and small dataframes to CSV files
    disproportionately_large.to_csv("disproportionately_large.csv", index=False)
    disproportionately_small.to_csv("disproportionately_small.csv", index=False)
    return disproportionately_large, disproportionately_small


#Not exactly proud of this process but learned a lot in the process
if __name__ == "__main__":
    disproportionately_large, disproportionately_small = main()
    print("Wards producing disproportionately large number of housing units:")
    print(disproportionately_large)
    print("Wards producing disproportionately small number of housing units:")
    print(disproportionately_small)
    