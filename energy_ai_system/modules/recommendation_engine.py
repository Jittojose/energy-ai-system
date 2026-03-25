class RecommendationEngine:
    def __init__(self, baseline_energy):
        self.baseline_energy = baseline_energy

    def generate_recommendation(
        self,
        predicted_energy,
        predicted_carbon,
        feature_importance,
        baseline_energy
    ):

        # --- Risk Level Determination ---
        if predicted_carbon > 2300:
            status = "High Carbon Risk"
            recommendations = [
                "Reduce active servers by 10%",
                "Improve cooling efficiency",
                "Consider renewable-backed grid usage"
            ]

        elif predicted_energy > baseline_energy:
            status = "Moderate Energy Usage"
            recommendations = [
                "Optimize workload distribution",
                "Shift non-critical tasks to off-peak hours",
                "Improve infrastructure insulation"
            ]

        else:
            status = "Efficient Operation"
            recommendations = [
                "Current configuration is energy efficient",
                "Maintain optimized workload settings"
            ]

        return {
            "status": status,
            "recommendations": recommendations
        }