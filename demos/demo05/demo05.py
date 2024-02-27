import seaborn as sns
import matplotlib.pyplot as plt

def plot_average_affordable_units_by_status(df):
    fig = plt.figure()
    ax = sns.barplot(df, x='MAR_WARD', y='TOTAL_AFFORDABLE_UNITS', hue="STATUS_PUBLIC")
    ax.set(
        xlabel=None, 
        ylabel='Average Affordable Units per Project'
    )
    plt.legend(title=None, frameon=False)
    sns.despine()
    return fig