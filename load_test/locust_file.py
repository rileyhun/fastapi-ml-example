from locust import HttpUser, task
import pandas as pd
import random
from sklearn import datasets

dataset = datasets.load_wine()
X = dataset.data
data = pd.DataFrame(X, columns=dataset.feature_names)
data = data.rename(columns={'od280/od315_of_diluted_wines': 'od_of_diluted_wines'})
data = data.to_dict(orient='records')

class WineModelPredictionUser(HttpUser):
    @task(1)
    def healthcheck(self):
        self.client.get("/healthcheck")

    @task(10)
    def prediction(self):
        record = random.choice(data).copy()
        self.client.post("/predict", json=record)

    @task(2)
    def prediction_bad_value(self):
        record = random.choice(data).copy()
        corrupt_key = random.choice(list(record.keys()))
        record[corrupt_key] = float("inf")
        self.client.post("/predict", json=record)