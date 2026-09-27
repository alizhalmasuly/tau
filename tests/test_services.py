import json
from io import BytesIO
from unittest.mock import patch

from django.test import SimpleTestCase

from ai_assistant.services import recommend_gear
from weather.services import get_weather


class DemoServiceTests(SimpleTestCase):
    @patch.dict("os.environ", {"AI_API_KEY": ""})
    def test_assistant_recommends_missing_gear_in_russian(self):
        reply = recommend_gear("У меня есть ботинки, вода и фонарь", language="ru")
        self.assertIn("аптечку первой помощи", reply)
        self.assertIn("Актуальная погода недоступна", reply)
        self.assertIn("ботинки, вода, фонарь", reply)
        self.assertNotIn("waterproof layer", reply)

    @patch.dict("os.environ", {"WEATHER_API_KEY": ""})
    def test_weather_without_key_reports_unavailable_instead_of_sample_data(self):
        data = get_weather()
        self.assertFalse(data["available"])
        self.assertEqual(data["error"], "missing_api_key")
        self.assertIsNone(data["temperature"])

    @patch.dict("os.environ", {"WEATHER_API_KEY": "sample-key"})
    @patch("weather.services.urlopen")
    def test_live_weather_uses_route_coordinates(self, urlopen):
        current = {
            "main": {"temp": 11, "feels_like": 9, "humidity": 50},
            "weather": [{"description": "clear", "id": 800}],
            "wind": {"speed": 2}, "visibility": 10000,
            "sys": {"sunrise": 3600, "sunset": 39600}, "timezone": 21600,
        }
        forecast = {"city": {"timezone": 21600}, "list": []}
        urlopen.side_effect = [
            BytesIO(json.dumps(current).encode()),
            BytesIO(json.dumps(forecast).encode()),
        ]

        data = get_weather(latitude=43.159, longitude=77.103)

        self.assertIn("lat=43.159", urlopen.call_args_list[0].args[0])
        self.assertIn("lon=77.103", urlopen.call_args_list[0].args[0])
        self.assertTrue(data["available"])
        self.assertEqual(data["sunrise"], "07:00")
        self.assertEqual(data["sunset"], "17:00")

    @patch.dict("os.environ", {"WEATHER_API_KEY": "sample-key"})
    @patch("weather.services.urlopen")
    def test_live_weather_includes_hourly_and_daily_forecasts(self, urlopen):
        current = {
            "main": {"temp": 11, "feels_like": 9, "humidity": 50},
            "weather": [{"description": "clear", "id": 800}],
            "wind": {"speed": 2}, "visibility": 10000, "timezone": 0,
        }
        period = {
            "dt": 1700000000,
            "main": {"temp": 10, "temp_min": 8, "temp_max": 12},
            "weather": [{"description": "clear", "id": 800}],
            "wind": {"speed": 3}, "pop": 0.25, "rain": {"3h": 0.2},
        }
        next_period = {**period, "dt": 1700086400, "main": {"temp": 7, "temp_min": 5, "temp_max": 9}}
        urlopen.side_effect = [
            BytesIO(json.dumps(current).encode()),
            BytesIO(json.dumps({"city": {"timezone": 0}, "list": [period, next_period]}).encode()),
        ]

        data = get_weather(latitude=43.123, longitude=77.456)

        self.assertEqual(len(data["hourly"]), 2)
        self.assertEqual(len(data["forecast"]), 2)
        self.assertEqual(data["hourly"][0]["precipitation_probability"], 25)
        self.assertEqual(data["forecast"][0]["temperature_min"], 8)