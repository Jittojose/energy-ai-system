class ScenarioEngine:
    def __init__(self, baseline):
        self.baseline = baseline

    def generate_scenario(self, scenario_type="baseline", workload_scale=1.0, temp_adjust=0):
        # Extract baseline values
        baseline_servers = self.baseline["avg_servers"]
        baseline_temp = self.baseline["avg_temperature"]
        baseline_sqft = self.baseline["avg_square_footage"]

        # Apply scenario-specific adjustments
        if scenario_type == "high_load":
            # High Load Scenario: Higher servers and temperature
            active_servers = baseline_servers * workload_scale * 1.5
            temperature = baseline_temp + temp_adjust + 2

        elif scenario_type == "optimized":
            # Optimized Scenario: Lower servers and temperature
            active_servers = baseline_servers * workload_scale * 0.7
            temperature = baseline_temp + temp_adjust - 1

        else:
            # Baseline Scenario: Standard scaling
            active_servers = baseline_servers * workload_scale
            temperature = baseline_temp + temp_adjust

        scenario_data = {
            "square_footage": float(baseline_sqft),
            "active_servers": float(active_servers),
            "temperature": float(temperature)
        }

        return scenario_data