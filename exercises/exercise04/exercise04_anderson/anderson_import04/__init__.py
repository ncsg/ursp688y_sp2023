#import packages
import pandas as pd

#def affordable_units_by_ward
def affordable_units_by_ward(info):
  affordable_table = {"Ward": ['Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6', 'Ward 7', 'Ward 8'], "Units": [0,0,0,0,0,0,0,0], "Ward Population":[0,0,0,0,0,0,0,0]}
  affordable_dataframe = pd.DataFrame(affordable_table)
  for ind in affordable_dataframe.index:
    affordable_dataframe.loc[ind,'Units'] = affordable_units_in_ward(affordable_dataframe.loc[ind,'Ward'],info),
    affordable_dataframe.loc[ind,'Ward Population'] = pop_in_ward(affordable_dataframe.loc[ind,'Ward'],info)
  #Unit value print statements
  highest_value = affordable_dataframe.loc[affordable_dataframe['Units'].idxmax()]
  smallest_value = affordable_dataframe.loc[affordable_dataframe['Units'].idxmin()]
  print("Information about affordable housing in wards:")
  print(f"{highest_value['Ward']} has the most ({highest_value['Units']}) 0-60% AMI units that are either under construction or in development.")
  print(f"{smallest_value['Ward']} has the least ({smallest_value['Units']}) 0-60% AMI units that are either under construction or in development.")
  #Add column for housing production
  affordable_dataframe['Affordable Housing Production'] = (affordable_dataframe['Units']/ affordable_dataframe['Ward Population']).round(3)
  #Housing production print statements
  print("\nInformation about housing production based on ward population:")
  highest_prop = affordable_dataframe.loc[affordable_dataframe['Affordable Housing Production'].idxmax()]
  lowest_prop = affordable_dataframe.loc[affordable_dataframe['Affordable Housing Production'].idxmin()]
  print(f"{lowest_prop['Ward']} is producing disproportionately small numbers of units ({lowest_prop['Affordable Housing Production']}) given their population ({lowest_prop['Ward Population']}).")
  print(f"{highest_prop['Ward']} is producing disproportionately large numbers of units ({highest_prop['Affordable Housing Production']}) given their population ({highest_prop['Ward Population']}).")
  def _color_red_or_green(val):
    color = 'red' if val < 0.025 else 'green'
    return 'color: %s' % color
  display(affordable_dataframe.style.applymap(_color_red_or_green, subset = pd.IndexSlice[:, ['Affordable Housing Production']]))
  return affordable_dataframe

#Iterate through to check for population in each ward
def pop_in_ward(ward, info):
  for ind in info.index:
    if is_in_ward(ind, ward, info):
      return info.loc[ind,'POP100']

#Pseudocode
# Make a counter for number of units
# Iterate over all rows in dataframe
#For each row will use functions to check if in ward and not completed
#If so, add results of affordable_units_in_project to counter
#Then return the counter

# def_affordable_units_in_ward returns the number of affordable units under construction
# or in development in a single, specified ward.
#Returns an integer.
# Calls is_project_completed, is_in_ward and affordable_units_in_project

def affordable_units_in_ward(ward, info):
  unit_amount = 0
  for ind in info.index:
    if is_in_ward(ind, ward, info) and not is_project_completed(ind, info):
      unit_amount += affordable_units_in_project(ind, info)
  return unit_amount

#Returns true if in a certain ward, and false otherwise.
def is_in_ward(project,ward,info):
  if info.loc[project, 'MAR_WARD'] == ward:
    return True
  else:
    return False

# Returns true if a housing project has already been completed, and false otherwise.
def is_project_completed(project, info):
  if info.loc[project,'STATUS_PUBLIC'] == 'Completed 2015 to Date':
    return True
  else:
    return False

# Returns the number of affordable units in a housing project available below 60 AMI.
def affordable_units_in_project(project, info):
  return (
  info.loc[project,'AFFORDABLE_UNITS_AT_0_30_AMI'] +
  info.loc[project,'AFFORDABLE_UNITS_AT_31_50_AMI'] +
  info.loc[project,'AFFORDABLE_UNITS_AT_51_60_AMI']
  )

