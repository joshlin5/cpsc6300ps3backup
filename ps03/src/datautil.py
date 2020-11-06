import os
import requests
import pandas as pd

def download_data(data_url, file_path):
    r = requests.get(data_url, verify=False)
    with open(file_path, "wb") as f:
        f.write(r.content)

def load_data(data_url, local_cached_datafile):
    if not os.path.exists(local_cached_datafile):
        if not os.path.exists(os.path.dirname(local_cached_datafile)):
            os.makedirs(os.path.dirname(local_cached_datafile))
        download_data(data_url, local_cached_datafile)
    return pd.read_csv(local_cached_datafile)

def load_housing_data():
    data_url = 'https://webapp02.palmetto.clemson.edu/dsci/datasets/housing/housing.csv'
    input_dir = os.path.join(os.getcwd(), 'input', 'housing.csv')
    return load_data(data_url, input_dir)
