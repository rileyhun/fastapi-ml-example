import requests
from sklearn import datasets
import pandas as pd
import random

url = "http://localhost:8080/api/v1/predict"
api_key = "secret"
headers = {'Auth': api_key, 'accept': 'application/json', 'Content-Type': 'application/json'}

dataset = datasets.load_wine()
X = dataset.data
data = pd.DataFrame(X, columns=dataset.feature_names)
data = data.rename(columns={'od280/od315_of_diluted_wines': 'od_of_diluted_wines'})
data = data.to_dict(orient='records')

for _ in range(10000):
    record = random.choice(data).copy()
    r = requests.post(url, headers=headers, json=record)
    print(r.text)



