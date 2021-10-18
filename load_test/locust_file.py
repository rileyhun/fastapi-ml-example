from locust import HttpUser, task
import pandas as pd
import random
import os

os.environ['AWS_ACCESS_KEY_ID'] = ""
os.environ['AWS_SECRET_ACCESS_KEY'] = ""
os.environ['AWS_SESSION_TOKEN'] = ""

df = pd.read_parquet("s3://ml_data/testset.parquet")
docs = df.to_dict(orient='records')

class AngelTierPredictionUser(HttpUser):
    @task(1)
    def healthcheck(self):
        self.client.get("/healthcheck")

    @task(10)
    def prediction(self):
        record = random.choice(docs).copy()
        self.client.post("/predict", json=record)

    @task(2)
    def prediction_bad_value(self):
        record = random.choice(docs).copy()
        corrupt_key = random.choice(list(record.keys()))
        record[corrupt_key] = float("inf")
        self.client.post("/predict", json=record)