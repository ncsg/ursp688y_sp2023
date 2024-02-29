def affordable_units_by_ward(housing_projects_with_pops):
    # filter data for relevant units and status
    filtered_df = housing_projects_with_pops[housing_projects_with_pops['STATUS_PUBLIC'].isin(['Under Construction', 'Pipeline'])]
    affordable_units_df = filtered_df[['MAR_WARD', 'P0010001','AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI', 'AFFORDABLE_UNITS_AT_51_60_AMI']]
    affordable_units_df = affordable_units_df.rename(columns={'MAR_WARD':'Ward', 'P0010001' : 'Total Population'})

    # calculate total affordable units at 60% AMI for each ward
    affordable_units_df.loc[:, 'Affordable Units >= 60% AMI'] = affordable_units_df[['AFFORDABLE_UNITS_AT_0_30_AMI', 'AFFORDABLE_UNITS_AT_31_50_AMI', 'AFFORDABLE_UNITS_AT_51_60_AMI']].sum(axis=1)

    # group by ward and aggregate
    ward_totals = affordable_units_df.groupby('Ward').agg({
      'Affordable Units >= 60% AMI': 'sum',
      'Total Population': 'sum'
    })

    # calculate units per 1000 people (to be comprehendable)
    ward_totals['Units Per 1,000 People'] = ward_totals['Affordable Units >= 60% AMI'] / (ward_totals['Total Population']/ 1000)

    #sort in descending order
    ward_totals = ward_totals.sort_values(by='Units Per 1,000 People', ascending=False)
    
    # select desired columns
    return ward_totals[['Units Per 1,000 People']]

# call the function
# result_df = affordable_units_by_ward(housing_projects_with_pops.copy())
# result_df