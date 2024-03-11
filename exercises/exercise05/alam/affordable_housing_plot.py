import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_affordable_housing(data, status=None, **kwargs):


    # Filter data by status if specified
    if status:
        data = data[data['STATUS_PUBLIC'] == status]

    # Data cleaning (assuming the logic remains the same)
    if 'MAR_WARD' in data.columns and not data.empty:
        data.loc[data['MAR_WARD'] == '1', 'MAR_WARD'] = 'Ward 1'
    
    # Group data by ward and sum the total number of affordable units
    ward_affordable_units = data.groupby('MAR_WARD')['TOTAL_AFFORDABLE_UNITS'].sum().reset_index()
    
    # Merge ward_affordable_units with the original DataFrame to get project status
    merged_data = pd.merge(ward_affordable_units, data[['MAR_WARD', 'STATUS_PUBLIC']], on='MAR_WARD', how='left')
   

    # Plot the data with hue based on project status
    plt.figure(figsize=(10, 6))
    ax=sns.barplot(x='MAR_WARD', y='TOTAL_AFFORDABLE_UNITS', data=data, hue='STATUS_PUBLIC', palette='viridis', estimator=sum)
    
    
    #Customize the plot
    plt.xlabel('Ward')
    plt.ylabel('Total Affordable Units')
    plt.title('Total Number of Affordable Housing Units by Ward')
    plt.legend(title='Project Status')
    
    
    
    plt.show()
        # Save the plot as a PNG file
    plt.savefig("housing_plot.png", format='png')

