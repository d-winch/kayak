from datetime import datetime


class Period():

    def __init__(self, data):
        self.data = data
        self.timestamp = self._get_timestamp()
        self.date = self._get_date()
        self.height = self._get_height()
        self.wind = self._get_wind()
        self.weather = self._get_weather()
        self.temp = self._get_temp()
        #self.x = 8

    def _get_timestamp(self):
        #ts = self.data.find_all("tr", class_="is-first")[0]
        ts = self.data.find_all('tr', {"data-forecast-day": True})[0]
        return int(ts['data-timestamp'])

    def _get_date(self):
        return datetime.fromtimestamp(self.timestamp)

    def _get_height(self):
        height = self.data.find_all(
            "td", class_="table-forecast-breaking-wave")[0]
        return height.get_text().strip()

    def _get_wind(self):
        wind = self.data.find_all("td", class_="table-forecast-wind")[0]
        wind = wind.get_text().strip().split(' ')
        wind = [w for w in wind if w != '']
        return f"{wind[0]}-{wind[1]} {wind[2]}"

    def _get_weather(self):
        weather = self.data.find_all(attrs={"data-filter": "weather"})[0]
        return weather['title'].strip()

    def _get_temp(self):
        temp = self.data.find_all("span", class_="unit")[1].parent
        return temp.get_text().strip()

    def __str__(self):
        return f"{self.date}, {self.timestamp}, {self.height}, {self.wind}, {self.weather}, {self.temp}"
