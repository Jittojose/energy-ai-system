# modules/comparison_engine.py

class ComparisonEngine:
    def __init__(self, ml_engine, carbon_engine):
        self.ml_engine = ml_engine
        self.carbon_engine = carbon_engine

    def evaluate(self, scenario_data):
        energy = self.ml_engine.predict_energy(scenario_data)
        carbon = self.carbon_engine.calculate_carbon(energy)

        return {
            "energy": round(energy, 2),
            "carbon": round(carbon, 2)
        }

    def compare_all(self, scenario_engine):
        scenarios = {
            "Baseline": scenario_engine.generate_scenario("baseline"),
            "High Load": scenario_engine.generate_scenario("high_load"),
            "Optimized": scenario_engine.generate_scenario("optimized")
        }

        results = {}

        for name, data in scenarios.items():
            results[name] = self.evaluate(data)

        return results