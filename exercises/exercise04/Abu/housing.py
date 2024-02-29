# Import dependencies
import pandas as pd

#create function
def john():

    # df = pd.read_csv('/content/drive/MyDrive/ursp688y_shared_data/ursp688y_shared_data/affordable_housing.csv')
    df = pd.read_csv('affordable_housing.csv')
    value_counts = df['STATUS_PUBLIC'].value_counts()
    value_counts

    # wd2 = pd.read_csv('/content/drive/MyDrive/ursp688y_shared_data/ursp688y_shared_data/Wards_from_2022.csv')
    wd2 = pd.read_csv('wards_from_2022.csv')
    wd2.head()

    filtered_df = df[(df["STATUS_PUBLIC"].str.contains("Under Construction")) | (df["STATUS_PUBLIC"].str.contains("Pipeline"))]
    #filtered_df
    # Select these three numerical columns, and the grouping columns
    ward_units_filtered=filtered_df[["MAR_WARD","AFFORDABLE_UNITS_AT_0_30_AMI", "AFFORDABLE_UNITS_AT_31_50_AMI", "AFFORDABLE_UNITS_AT_51_60_AMI"]]

    #Group units under wards
    ward_units = filtered_df.groupby("MAR_WARD")[["AFFORDABLE_UNITS_AT_0_30_AMI", "AFFORDABLE_UNITS_AT_31_50_AMI", "AFFORDABLE_UNITS_AT_51_60_AMI"]].sum()
    ward_units

    #Add ward units under 60%
    ward_units_filtered["TOTAL_AFFORDABLE_UNITS_UP_TO_60%_AMI"] = ward_units_filtered["AFFORDABLE_UNITS_AT_0_30_AMI"] + ward_units_filtered["AFFORDABLE_UNITS_AT_31_50_AMI"]+ward_units_filtered["AFFORDABLE_UNITS_AT_51_60_AMI"]
    ward_units_filtered_sum=ward_units_filtered.groupby(["MAR_WARD"])["TOTAL_AFFORDABLE_UNITS_UP_TO_60%_AMI"].agg('sum')

    #join the data set together
    housing_projects_with_pops = pd.merge(ward_units_filtered_sum, wd2, left_on='MAR_WARD', right_on='NAME')

    housing_projects_with_pops = pd.merge(
        ward_units_filtered_sum,
        wd2[['NAME','POP100','HU100']],
        left_on='MAR_WARD',
        right_on='NAME')
    #print(housing_projects_with_pops)

    #calculate unit for each population
    housing_projects_with_pops['housing_projects_per_pop'] = housing_projects_with_pops['TOTAL_AFFORDABLE_UNITS_UP_TO_60%_AMI'] / housing_projects_with_pops['POP100']
    housing_projects_with_pops

    return housing_projects_with_pops