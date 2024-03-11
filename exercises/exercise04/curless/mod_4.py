import pandas as pd 

def combined_data():
    a_h = pd.read_csv('affordable_housing.csv')
    ward_dems = pd.read_csv('wards_from_2022.csv')

#adding code cause changing 1 to ward 1 makes merging the rows easier
    idx = a_h[a_h['MAR_WARD'] == '1'].index[0]
    a_h.at[idx, 'MAR_WARD'] = 'Ward 1'

#merging and left_on right_on is important because they share data that you can merge from
    a_h = a_h.merge(ward_dems[['NAME','POP100']], 
    left_on='MAR_WARD', right_on='NAME')

#copying data from exercise 3
    #step 1, summing AMIs
    a_h['AMI'] = a_h['AFFORDABLE_UNITS_AT_0_30_AMI'] + a_h['AFFORDABLE_UNITS_AT_31_50_AMI'] + a_h['AFFORDABLE_UNITS_AT_51_60_AMI']
    #step 2, filtering by status
    a_h = a_h[a_h['STATUS_PUBLIC'].isin(['Under Construction','In Development'])]
    ward_sums = a_h.groupby('MAR_WARD')['AMI'].sum().reset_index()

    return ward_sums