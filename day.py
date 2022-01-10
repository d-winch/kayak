from datetime import datetime
from bs4 import BeautifulSoup, Tag  # type: ignore
from typing import List, Set, Tuple, Dict, Any


class Day():

    def __init__(self, data: Tag):
        self.rows = data.find_all('tr')[1:8]
        #self.timestamp = self._get_timestamp()
        #self.date = self._get_date()
        #self.height = self._get_height()
        #self.wind = self._get_wind()
        #self.weather = self._get_weather()
        #self.temp = self._get_temp()
        self.forecast = self.get_forecast()

    def _get_timestamp(self, row: Tag) -> int:
        #ts = self.data.find_all('tr', {"data-forecast-day": True})[0]
        # return int(ts['data-timestamp'])
        return int(row['data-timestamp'])

    def _get_datetime(self, timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp)

    def _get_height(self, row: Tag) -> str:
        height = row.find_all("td", class_="table-forecast-breaking-wave")[0]
        return height.get_text().strip()

    def _get_wind(self, row: Tag) -> tuple:
        wind = row.find_all("td", class_="table-forecast-wind")[0]
        wind = wind.get_text().strip().split(' ')
        wind = [w for w in wind if w != '']
        # return f"{wind[0]}-{wind[1]} {wind[2]}"
        return int(wind[0]), int(wind[1])

    def _get_weather(self, row: Tag) -> str:
        weather = row.find_all(attrs={"data-filter": "weather"})[0]
        return weather['title'].strip()

    def _get_temp(self, row: Tag) -> int:
        #temp = self.data.find_all("span", class_="unit")[1].parent
        temp = row.find_all("span", class_="unit")[1].parent
        return int(temp.get_text().strip()[:-2])  # Remove degrees c

    # def __str__(self):
    #    return f"{self.date}, {self.timestamp}, {self.height}, {self.wind}, {self.weather}, {self.temp}"

    def get_forecast(self) -> List[List[Any]]:
        forecast = []
        for row in self.rows:
            timestamp = self._get_timestamp(row)
            datetime = self._get_datetime(timestamp)
            height = self._get_height(row)
            wind_steady, wind_gust = self._get_wind(row)
            weather = self._get_weather(row)
            temp = self._get_temp(row)
            forecast.append([timestamp, datetime, height,
                            wind_steady, wind_gust, weather, temp])
        return forecast
