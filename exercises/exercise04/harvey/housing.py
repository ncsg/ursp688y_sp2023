import pandas as pd

def calc_affordable_housing_per_ward():

    ## Build a tidy dataframe with everything I need to solve the problem in it

    # Load the data
    affordable_housing = pd.read_csv('affordable_housing.csv')
    ward_demogs = pd.read_csv('wards_from_2022.csv')

    # Data cleaning: replace '1' with 'Ward 1' for one record
    idx = affordable_housing[affordable_housing['MAR_WARD'] == '1'].index[0]
    affordable_housing.at[idx, 'MAR_WARD'] = 'Ward 1'

    # Join population data
    affordable_housing = affordable_housing.merge(
        ward_demogs[['NAME','POP100']], 
        left_on='MAR_WARD', 
        right_on='NAME',
        )

    # Filter under construction and pipeline projects
    affordable_housing = affordable_housing[
        affordable_housing['STATUS_PUBLIC'].isin(['Under Construction', 'Pipeline'])
        ]

    # Sum units at 0-60% AMI 
    cols = [
        'AFFORDABLE_UNITS_AT_0_30_AMI',
        'AFFORDABLE_UNITS_AT_31_50_AMI',
        'AFFORDABLE_UNITS_AT_51_60_AMI',
    ]
    affordable_housing['AFFORDABLE_UNITS_AT_0_60_AMI'] = affordable_housing[cols].sum(axis=1)

    ## Now that all my data are together, I can start analyzing them

    # Sum units within wards
    affordable_housing_per_ward = affordable_housing.groupby('MAR_WARD').agg({
        'AFFORDABLE_UNITS_AT_0_60_AMI': 'sum',
        'POP100': 'first',
        })

    # Calculate units per population
    affordable_housing_per_ward['units_per_pop'] = (
        affordable_housing_per_ward['AFFORDABLE_UNITS_AT_0_60_AMI'] / 
        affordable_housing_per_ward['POP100']
    )

    # Tidy up my results by changing column names and filtering to only the columns I need
    affordable_housing_per_ward = affordable_housing_per_ward.reset_index()
    cols = {
        'MAR_WARD': 'Ward',
        'AFFORDABLE_UNITS_AT_0_60_AMI': 'Affordable Units',
        'units_per_pop': 'Affordable Units per Population'
    }
    affordable_housing_per_ward = affordable_housing_per_ward.rename(columns=cols)
    affordable_housing_per_ward = affordable_housing_per_ward[cols.values()]

    return affordable_housing_per_ward