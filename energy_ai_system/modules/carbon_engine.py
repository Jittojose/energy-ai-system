class CarbonEngine:
    def __init__(self, emission_factor=0.475):
        self.emission_factor = emission_factor

    def calculate_carbon(self, energy_kwh):
        carbon = energy_kwh * self.emission_factor
        return carbon