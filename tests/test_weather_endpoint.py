from unittest.mock import patch

from django.test import SimpleTestCase


class WeatherEndpointTests(SimpleTestCase):
    @patch("weather.views.get_weather", return_value={"available": True, "temperature": 8})
    def test_weather_api_uses_selected_coordinates(self, get_weather):
        response = self.client.get("/weather/api/?lat=27.9881&lon=86.925")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["temperature"], 8)
        get_weather.assert_called_once_with(latitude=27.9881, longitude=86.925, language="ru")

    def test_weather_api_rejects_invalid_coordinates(self):
        response = self.client.get("/weather/api/?lat=100&lon=0")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "invalid_coordinates")