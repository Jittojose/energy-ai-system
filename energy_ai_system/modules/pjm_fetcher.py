import requests
import pandas as pd

class PJMFetcher:
    def __init__(self):
        self.base_url = "https://api.pjm.com/api/v1/"

    def fetch_sample_data(self):
        # For now simulate simple time-series
        # Later you can use real API key

        dates = pd.date_range(start="2024-01-01", periods=100, freq="h")
        demand = [1000 + i*2 for i in range(100)]

        df = pd.DataFrame({
            "datetime": dates,
            "energy_mw": demand
        })

        print("PJM sample data generated.")
        return df