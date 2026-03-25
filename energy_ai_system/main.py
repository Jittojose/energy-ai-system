import pandas as pd

from modules.data_loader import DataLoader
from modules.baseline_engine import BaselineEngine
from modules.pjm_fetcher import PJMFetcher
from modules.scenario_engine import ScenarioEngine
from modules.ml_engine import MLEngine
from modules.carbon_engine import CarbonEngine
from modules.xai_engine import XAIEngine
from modules.forecast_engine import ForecastEngine


print("\n==============================================")
print(" AI-Powered Energy & Carbon Forecasting System ")
print("==============================================\n")


# -------------------------------------------------
# 1️⃣ Load Kaggle Dataset
# -------------------------------------------------
loader = DataLoader("data/kaggle_energy.csv")
df = loader.load_data()
df = loader.clean_data()


# -------------------------------------------------
# 2️⃣ Extract Baseline
# -------------------------------------------------
baseline_engine = BaselineEngine(df)
baseline = baseline_engine.extract_baseline()


# -------------------------------------------------
# 3️⃣ Fetch PJM Time-Series Data
# -------------------------------------------------
pjm = PJMFetcher()
pjm_data = pjm.fetch_sample_data()


# -------------------------------------------------
# 4️⃣ Generate Scenario
# -------------------------------------------------
scenario_engine = ScenarioEngine(baseline)

scenario_data = scenario_engine.generate_scenario(
    scenario_type="high_load",   # change to baseline / optimized
    workload_scale=1.1,
    temp_adjust=1
)


# -------------------------------------------------
# 5️⃣ Train & Load ML Model
# -------------------------------------------------
ml_engine = MLEngine(df)
ml_engine.train_model()
ml_engine.load_model()

predicted_energy = ml_engine.predict_energy(scenario_data)


# -------------------------------------------------
# 6️⃣ Carbon Estimation
# -------------------------------------------------
carbon_engine = CarbonEngine()
predicted_carbon = carbon_engine.calculate_carbon(predicted_energy)


# -------------------------------------------------
# 7️⃣ Explainable AI
# -------------------------------------------------
xai_engine = XAIEngine(ml_engine.model)

feature_names = ["square_footage", "active_servers", "temperature"]
importance = xai_engine.get_feature_importance(feature_names)
top_feature = xai_engine.get_top_feature(importance)


# -------------------------------------------------
# 8️⃣ Prophet Forecasting
# -------------------------------------------------
forecast_engine = ForecastEngine(df)

ts_df = forecast_engine.prepare_time_series()
forecast_engine.train_model(ts_df)

future_forecast = forecast_engine.forecast_future(periods=15)


# =================================================
# 🔥 STRUCTURED OUTPUT FOR SECOND REVIEW
# =================================================

print("\n==============================")
print("   SCENARIO DETAILS")
print("==============================")
print(f"Square Footage      : {scenario_data['square_footage']:.2f}")
print(f"Active Servers      : {scenario_data['active_servers']:.2f}")
print(f"Temperature (°C)    : {scenario_data['temperature']:.2f}")

print("\n==============================")
print("   MODEL PERFORMANCE")
print("==============================")
print(f"R2 Score            : {ml_engine.r2_score_value:.3f}")
print(f"Mean Absolute Error : {ml_engine.mae_value:.2f} kWh")

print("\n==============================")
print("   ENERGY PREDICTION")
print("==============================")
print(f"Predicted Energy    : {predicted_energy:.2f} kWh")
print(f"Estimated Carbon    : {predicted_carbon:.2f} kg CO2")

print("\n==============================")
print("   EXPLAINABLE AI")
print("==============================")
for feature, value in importance.items():
    print(f"{feature:<20} : {float(value):.2f}%")

print(f"\nMost Influential Factor : {top_feature}")

print("\n==============================")
print("   FUTURE ENERGY FORECAST (Last 5 Days)")
print("==============================")
print(future_forecast.tail(5))

print("\n==============================================")
print(" System Execution Completed Successfully ")
print("==============================================\n")