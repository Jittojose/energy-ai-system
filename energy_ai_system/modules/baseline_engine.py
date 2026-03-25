class BaselineEngine:
    def __init__(self, df):
        self.df = df

    def extract_baseline(self):
        baseline = {
            "avg_square_footage": float(self.df["square_footage"].mean()),
            "avg_servers": float(self.df["active_servers"].mean()),
            "avg_temperature": float(self.df["temperature"].mean()),
            "avg_energy": float(self.df["energy_kwh"].mean())
        }

        print("Baseline extracted dynamically.")
        return baseline