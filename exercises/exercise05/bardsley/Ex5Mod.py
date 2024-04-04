def ward_affordable_sum_graph(columns_list,mask_column):
  import pandas as pd
  from matplotlib import pyplot as plt
  import seaborn as sns
  sns.set_style('dark')
  df = pd.read_csv('affordable_housing.csv')
  df_mask = df[(df['STATUS_PUBLIC'] == mask_column)]
  #sum horizontally across the three affordability columns
  df_mask['ProjectUnits'] = df_mask[columns_list].sum(axis=1)
  graph = sns.countplot(df_mask,x='MAR_WARD',order=df['MAR_WARD'].value_counts().index)
  return graph


#I was going to try to do something harder than this, but I got stuck and ran out of time. I wanted to melt
#the data and then have the bar graph colored by the AMI level of affordability.
#df_melt = pd.melt(
  #  df_mask,
  #  id_vars=['OBJECTID','MAR_WARD','STATUS_PUBLIC'],
  #  value_vars=['AFFORDABLE_UNITS_AT_0_30_AMI','AFFORDABLE_UNITS_AT_31_50_AMI','AFFORDABLE_UNITS_AT_51_60_AMI'],
  #  var_name='Affordability_Level',
  #  value_name='Units'
#)
#x1=df_melt['MAR_WARD'].unique()
#y1=df_melt.groupby('MAR_WARD')['Units'].sum().reset_index()
#plt.figure(figsize=(8,6))
#sns.boxplot(data=df_melt, x=x1,y=y1)