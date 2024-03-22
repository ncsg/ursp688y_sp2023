import pandas as pd
import seaborn as sb

def ami_to_con_ward():
    affordable_housing = pd.read_csv('affordable_housing.csv')
    idx = affordable_housing[affordable_housing['MAR_WARD'] == '1'].index[0]
    affordable_housing.at[idx, 'MAR_WARD'] = 'Ward 1'

    small_data_set = affordable_housing[['MAR_WARD','STATUS_PUBLIC','TOTAL_AFFORDABLE_UNITS']]
    status_filter = small_data_set[small_data_set['STATUS_PUBLIC'].isin(['Under Construction'])]

    data_plot = pd.DataFrame(status_filter.groupby('MAR_WARD')['TOTAL_AFFORDABLE_UNITS'].sum())
    sb.barplot(data = data_plot , x = 'MAR_WARD' , y = 'TOTAL_AFFORDABLE_UNITS')

    return status_filter