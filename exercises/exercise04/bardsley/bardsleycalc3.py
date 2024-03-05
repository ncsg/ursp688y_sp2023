import pandas as pd

def WardPipelineSum(column1,column2,column3):
    housing_projects = pd.read_csv('affordable_housing_Bardsley.csv')
    ward_pop = pd.read_csv('wards_from_2022.csv')
    housing_projects_with_pops = pd.merge(housing_projects, ward_pop[['NAME', 'POP100','HU100']], left_on= 'MAR_WARD', right_on= 'NAME')
    # df = pd.DataFrame(housing_projects_with_pops)
    df = housing_projects_with_pops
    #create a mask to filter for rows that are in the pipeline or under construction
    df_mask = df[(df['STATUS_PUBLIC'] == 'Under Construction') | (df['STATUS_PUBLIC'] == 'Pipeline')]
    #sum horizontally across the three affordability columns
    df_mask['ColumnSum'] = df_mask[[column1,column2,column3]].sum(axis=1)
    #use grouping to get the sum for each ward:
    ward_sum = df_mask.groupby('MAR_WARD')['ColumnSum'].sum().sort_values()
    totalsdf = pd.DataFrame({'Ward':ward_sum.index, 'Pop':ward_sum.values})
    totalsdf['HousingPerPop'] = totalsdf['Pop'] / housing_projects_with_pops['POP100']   
    return totalsdf