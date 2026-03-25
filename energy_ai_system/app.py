from flask import Flask, render_template, request, session, send_file
from flask_session import Session
import tempfile
import os
from datetime import datetime

from modules.data_loader import DataLoader
from modules.baseline_engine import BaselineEngine
from modules.scenario_engine import ScenarioEngine
from modules.ml_engine import MLEngine
from modules.carbon_engine import CarbonEngine
from modules.xai_engine import XAIEngine
from modules.forecast_engine import ForecastEngine
from modules.comparison_engine import ComparisonEngine
from modules.recommendation_engine import RecommendationEngine
from modules.pdf_generator import PDFGenerator

app = Flask(__name__)

# Configure session
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SESSION_TYPE'] = 'filesystem'
# Store server-side session files in a temp directory (avoid colliding with a local "flask_session" folder)
app.config['SESSION_FILE_DIR'] = os.path.join(tempfile.gettempdir(), 'flask_session')
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
Session(app)

# =====================================================
# 🔹 INITIALIZE SYSTEM (Runs once at startup)
# =====================================================

# Load dataset
loader = DataLoader("data/kaggle_energy.csv")
df = loader.load_data()
df = loader.clean_data()

# Extract baseline
baseline_engine = BaselineEngine(df)
baseline = baseline_engine.extract_baseline()

# Train & load ML model
ml_engine = MLEngine(df)
ml_engine.train_model()
ml_engine.load_model()

# Initialize carbon engine
carbon_engine = CarbonEngine()


# =====================================================
# 🔹 ROUTES
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/guide")
def guide():
    return render_template("guide.html")


@app.route("/predict", methods=["POST"])
def predict():

    # -------------------------------------------------
    # 1️⃣ Get User Inputs
    # -------------------------------------------------
    scenario_type = request.form["scenario"]
    workload_scale = float(request.form["workload"])
    temp_adjust = float(request.form["temperature"])

    # -------------------------------------------------
    # 2️⃣ Generate Scenario Data
    # -------------------------------------------------
    scenario_engine = ScenarioEngine(baseline)

    scenario_data = scenario_engine.generate_scenario(
        scenario_type=scenario_type,
        workload_scale=workload_scale,
        temp_adjust=temp_adjust
    )

    # -------------------------------------------------
    # 3️⃣ Predict Energy & Carbon
    # -------------------------------------------------
    predicted_energy = ml_engine.predict_energy(scenario_data)
    predicted_carbon = carbon_engine.calculate_carbon(predicted_energy)

    # -------------------------------------------------
    # 4️⃣ Explainable AI (Feature Importance)
    # -------------------------------------------------
    xai_engine = XAIEngine(ml_engine.model)
    feature_names = ["square_footage", "active_servers", "temperature"]

    importance = xai_engine.get_feature_importance(feature_names)
    top_feature = xai_engine.get_top_feature(importance)

    # -------------------------------------------------
    # 5️⃣ Scenario Comparison (Baseline vs High vs Optimized)
    # -------------------------------------------------
    comparison_engine = ComparisonEngine(ml_engine, carbon_engine)
    comparison_results = comparison_engine.compare_all(scenario_engine)

    # -------------------------------------------------
    # 6️⃣ Future Energy Forecast (Prophet)
    # -------------------------------------------------
    forecast_engine = ForecastEngine(df)
    ts_df = forecast_engine.prepare_time_series()
    forecast_engine.train_model(ts_df)

    future_forecast = forecast_engine.forecast_future(periods=15)
    last_15 = future_forecast.tail(15)

    forecast_dates = last_15["ds"].dt.strftime("%Y-%m-%d").tolist()
    forecast_values = last_15["yhat"].round(2).tolist()
    
    # AI Forecast Analysis
    min_energy = last_15["yhat"].min()
    max_energy = last_15["yhat"].max()
    avg_energy = last_15["yhat"].mean()
    
    # Determine trend
    first_half = last_15["yhat"].head(7).mean()
    second_half = last_15["yhat"].tail(8).mean()
    if second_half > first_half * 1.05:
        trend = "increasing"
    elif second_half < first_half * 0.95:
        trend = "decreasing"
    else:
        trend = "stable"
    
    forecast_analysis = f"The forecast indicates that energy consumption will range between {min_energy:.0f} and {max_energy:.0f} kWh over the next 15 days, suggesting {trend} operational demand."

    # -------------------------------------------------
    # 7 AI Operational Recommendation
    # -------------------------------------------------
    recommendation_engine = RecommendationEngine(baseline["avg_energy"])
    recommendation_result = recommendation_engine.generate_recommendation(
        predicted_energy=predicted_energy,
        predicted_carbon=predicted_carbon,
        feature_importance=importance,
        baseline_energy=baseline["avg_energy"]
    )

    # Store data in session for PDF generation
    session['report_data'] = {
        'scenario_type': scenario_type,
        'workload_scale': workload_scale,
        'temperature_adjustment': temp_adjust,
        'energy': round(predicted_energy, 2),
        'carbon': round(predicted_carbon, 2),
        'importance': importance,
        'top_feature': top_feature,
        'comparison': comparison_results,
        'forecast_dates': forecast_dates,
        'forecast_values': forecast_values,
        'forecast_analysis': forecast_analysis,
        'recommendation': recommendation_result
    }

    # -------------------------------------------------
    # 8 Render Result Page
    # -------------------------------------------------
    return render_template(
        "result.html",
        energy=round(predicted_energy, 2),
        carbon=round(predicted_carbon, 2),
        importance=importance,
        top_feature=top_feature,
        comparison=comparison_results,
        forecast_dates=forecast_dates,
        forecast_values=forecast_values,
        forecast_analysis=forecast_analysis,
        recommendation=recommendation_result,
    )


@app.route("/download-report")
def download_report():
    """Generate and download PDF report"""
    
    # Check if report data exists in session
    if 'report_data' not in session:
        return "No report data available. Please run a prediction first.", 400
    
    report_data = session['report_data']
    
    try:
        # Generate PDF
        pdf_generator = PDFGenerator()
        pdf_content = pdf_generator.generate_report(report_data)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_content)
            tmp_file_path = tmp_file.name
        
        # Send file and cleanup
        def remove_file(response):
            try:
                os.unlink(tmp_file_path)
            except Exception:
                pass
            return response
        
        return send_file(
            tmp_file_path,
            as_attachment=True,
            download_name=f"AI_Energy_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500


# =====================================================
# 🔹 RUN APP
# =====================================================

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
