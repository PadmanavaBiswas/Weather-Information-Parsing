import csv
import datetime
import time
from pathlib import Path

import requests

from Load_env import MY_API_KEY
from Logging import My_logger


class Weather_Details:
    def __init__(self, locations):
        self.locations = locations
        self.logger = My_logger()

        self.csv_file = Path("../output/weather_details.csv").absolute()
        self.headers = [
            "SL.",
            "Fetched At",
            "City",
            "Country",
            "Timezone",
            "Weather",
            "Weather Desc.",
            "Temp (Deg. C)",
            "Wind Speed (Km/h)",
        ]
        sl = self.check_storage()

        self.request_to_api(sl)

    def check_storage(self):
        file_exist = self.csv_file.is_file()

        if not file_exist:
            with open(self.csv_file, "w") as wd_file:
                csv_writer = csv.DictWriter(
                    wd_file, fieldnames=self.headers, delimiter=","
                )
                csv_writer.writeheader()

            return 0

        with open(self.csv_file, "r") as wd_file:
            rows = list(csv.reader(wd_file))

        return int(rows[-1][0]) if len(rows) > 1 else 0

    def request_to_api(self, sl):
        for i, loc in enumerate(self.locations, start=sl + 1):
            payload = {"q": loc, "appid": MY_API_KEY, "units": "metric"}

            try:
                req = requests.get(
                    "https://api.openweathermap.org/data/2.5/weather",
                    params=payload,
                    timeout=10,
                )
            except requests.exceptions.ConnectionError as e:
                self.logger.log_critical(f"Connection failed for {loc}: {e}")
            except requests.exceptions.Timeout as e:
                self.logger.log_critical(f"Connection timeout for {loc}: {e}")
            except requests.exceptions.RequestException as e:
                self.logger.log_critical(f"Error occuered for {loc}: {e}")
            else:
                self.store_data(req, i, loc)

            time.sleep(0.3)

    def store_data(self, req, i, loc):
        if req.status_code != 200:
            self.logger.log_critical(f"{loc} not found")
            return

        self.logger.log_info(
            f"Fetched {loc} details in {req.elapsed.total_seconds()} seconds"
        )

        fetched_data = req.json()
        fetched_at = f"{datetime.datetime.now().astimezone():%Y-%m-%d;%H:%M:%S}"

        timezone = fetched_data["timezone"]
        hours = timezone // 3600
        minutes = (abs(timezone) % 3600) // 60
        timezone_str = (
            f"UTC{'+' if timezone >= 0 else '-'}{abs(hours):02d}:{minutes:02d}"
        )

        with open(self.csv_file, "a") as wd_file:
            csv_writer = csv.DictWriter(wd_file, fieldnames=self.headers, delimiter=",")
            csv_writer.writerow(
                {
                    "SL.": i,
                    "Fetched At": fetched_at,
                    "City": fetched_data["name"],
                    "Country": fetched_data["sys"]["country"],
                    "Timezone": timezone_str,
                    "Weather": fetched_data["weather"][0]["main"],
                    "Weather Desc.": fetched_data["weather"][0]["description"],
                    "Temp (Deg. C)": fetched_data["main"]["temp"],
                    "Wind Speed (Km/h)": fetched_data["wind"]["speed"],
                }
            )


if __name__ == "__main__":
    locations = [
        "Barrackpore,WestBengal,India",
        "Udaipur,Rajasthan,India",
        "Noida,Delhi,India",
        "Leh,Ladakh,India",
        "Guwahati,Assam,India",
    ]
    wd = Weather_Details(locations)
