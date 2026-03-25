import pandas as pd

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.filepath)
        print("Dataset loaded successfully.")
        return self.df

    def clean_data(self):
        self.df = self.df.dropna()
        print("Missing values removed.")
        return self.df

    def get_dataframe(self):
        return self.df