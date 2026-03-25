import pandas as pd
from prophet import Prophet

class ForecastEngine:
    def __init__(self, df):
        self.df = df
        self.model = None

    def prepare_time_series(self):
        # Create synthetic time index
        self.df = self.df.copy()
        self.df["ds"] = pd.date_range(start="2024-01-01", periods=len(self.df), freq="D")
        self.df["y"] = self.df["energy_kwh"]

        return self.df[["ds", "y"]]

    def train_model(self, ts_df):
        self.model = Prophet()
        self.model.fit(ts_df)
        print("Prophet model trained successfully.")

    def forecast_future(self, periods=30):
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)

        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]