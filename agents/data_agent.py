import requests
import json


class DataAgent:
    def __init__(self, epi_data_path="data/epi_reference.json"):
        self.coordinates = {
            "Colombo": (6.9271, 79.8612),
            "Gampaha": (7.0917, 79.9992),
            "Kalutara": (6.5854, 79.9607),
            "Jaffna": (9.6615, 80.0255)
        }
        with open(epi_data_path, "r") as f:
            self.epi_data = json.load(f)

    def get_weather_data(self, district):
        if district not in self.coordinates:
            raise ValueError("District not found.")
        latitude, longitude = self.coordinates[district]
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            f"&current=temperature_2m&daily=precipitation_sum"
            f"&forecast_days=1&timezone=auto"
        )
        response = requests.get(url)
        data = response.json()
        return {
            "temperature_c": data["current"]["temperature_2m"],
            "rainfall_mm": data["daily"]["precipitation_sum"][0]
        }

    def get_case_data(self, district):
        cases = self.epi_data.get(district, 0)
        return {"cases_last_week": cases}

    def analyze_district(self, district):
        weather = self.get_weather_data(district)
        epidemiological = self.get_case_data(district)
        return {
            "district": district,
            "weather": weather,
            "epidemiological": epidemiological
        }


if __name__ == "__main__":
    agent = DataAgent()
    for district in ["Colombo", "Gampaha", "Jaffna", "Kalutara"]:
        result = agent.analyze_district(district)
        print(result)