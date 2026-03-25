import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error


class MLEngine:
    def __init__(self, df):
        self.df = df
        self.model = None
        self.r2_score_value = None
        self.mae_value = None

    def train_model(self):
        # Select features and target
        X = self.df[["square_footage", "active_servers", "temperature"]]
        y = self.df["energy_kwh"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Initialize model
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        # Train model
        self.model.fit(X_train, y_train)

        # Evaluate model
        y_pred = self.model.predict(X_test)

        self.r2_score_value = r2_score(y_test, y_pred)
        self.mae_value = mean_absolute_error(y_test, y_pred)

        print("Model trained and saved successfully.")
        print(f"Model R2 Score: {self.r2_score_value:.3f}")
        print(f"Model MAE: {self.mae_value:.2f}")

        # Save model
        joblib.dump(self.model, "models/energy_model.pkl")

    def load_model(self):
        self.model = joblib.load("models/energy_model.pkl")
        print("Model loaded successfully.")

    def predict_energy(self, scenario_data):
        input_df = pd.DataFrame([scenario_data])
        prediction = self.model.predict(input_df)[0]
        return float(prediction)