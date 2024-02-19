import pandas as pd

def load_affordable_housing():
    df = pd.read_csv('affordable_housing.csv')
    return df