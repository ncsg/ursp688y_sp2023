#import packages
import pandas as pd
import os

#Connect and mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

#Check working directory
#os.getcwd()

#Set working directory
wd_path = '/content/drive/MyDrive/exercise05_anderson'
os.chdir(wd_path)
os.path.isfile('affordable_housing.csv')

def plot_affordable_units_by_ward(info, completion_state=None):
  affordable_table = {"Ward": ['Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6', 'Ward 7', 'Ward 8'], "Total Affordable Units": [0,0,0,0,0,0,0,0]}
  affordable_dataframe = pd.DataFrame(affordable_table)
  for ind in affordable_dataframe.index:
    title = 'Total Affordable Units by Ward'
    if completion_state!=None:
      info=info.loc[info['STATUS_PUBLIC']==completion_state]
      title += ': ' + completion_state
    affordable_dataframe.loc[ind,'Total Affordable Units'] = affordable_units_in_ward(affordable_dataframe.loc[ind,'Ward'],info)
  affordable_dataframe.plot.bar(x='Ward',y='Total Affordable Units',title=title,ylabel='# Units')

def affordable_units_in_ward(ward, info):
  unit_amount = 0
  for ind in info.index:
    if is_in_ward(ind, ward, info):
      unit_amount += info.loc[ind,'TOTAL_AFFORDABLE_UNITS']
  return unit_amount

#Returns true if in a certain ward, and false otherwise.
def is_in_ward(project,ward,info):
  if info.loc[project, 'MAR_WARD'] == ward:
    return True
  else:
    return False