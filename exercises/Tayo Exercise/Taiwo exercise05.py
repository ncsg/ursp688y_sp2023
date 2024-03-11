import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_housing_data(file_path):
    if not os.path.isfile(file_path):
        print(f"File does not exist: {file_path}")
        return None

    housing_project = pd.read_csv(file_path)
    
    housing_project.at[housing_project[housing_project['MAR_WARD'] == '1'].index[0], 'MAR_WARD'] = 'Ward 1'
    
    return housing_project

def plot_project_status_by_ward(housing_project):
    sns.set_style('white')
    fig, ax = plt.subplots(figsize=(12, 8))
    housing_project['MAR_WARD'].value_counts().plot(kind='bar', ax=ax)
    plt.title('Project Status by Ward')
    plt.xlabel('Wards')
    plt.ylabel('Number of Projects')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_affordable_units_by_ward(housing_project, status_category, ami_range):
    housing_project_filtered = housing_project[housing_project['STATUS_PUBLIC'] == status_category]
    column_name = f"AFFORDABLE_UNITS_AT_{ami_range}_AMI"
    ward_stats = housing_project_filtered.groupby('MAR_WARD')[column_name].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.bar(ward_stats['MAR_WARD'], ward_stats[column_name], color='Crimson')
    plt.title(f'Mean Affordable Units at {ami_range}% AMI by Ward for {status_category} Projects')
    plt.xlabel('Ward')
    plt.ylabel(f'Mean Affordable Units at {ami_range}% AMI')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

file_path = '/content/drive/MyDrive/Tayo Exercise/affordable_housing.csv'
housing_project = load_and_prepare_housing_data(file_path)
if housing_project is not None:
    plot_project_status_by_ward(housing_project)
    plot_affordable_units_by_ward(housing_project, 'Under Construction', '0_30')
