import better_exceptions
import pandas as pd  # type: ignore
import requests
from bs4 import BeautifulSoup, Tag  # type: ignore
from rich import print
from tabulate import tabulate

from day import Day

better_exceptions.hook()


class KayakParser():

    def __init__(self, url: str):
        page = requests.get(url)
        if page.status_code == 200:
            self.soup = BeautifulSoup(page.content, 'html.parser')
        else:
            print(page.status_code, 'Exiting')
            exit()

    def get_report_table(self) -> Tag:
        return self.soup.find_all("table", class_="table table-primary table-forecast allSwellsActive msw-js-table")[0]

    def get_days(self, surf_table: Tag) -> Tag:
        return surf_table.find_all("tbody")


if __name__ == '__main__':

    URL = 'https://magicseaweed.com/Newquay-Fistral-North-Surf-Report/1/'
    URL = "https://magicseaweed.com/Falmouth-Surf-Report/135/"

    k = KayakParser(URL)
    surf_table = k.get_report_table()
    days = k.get_days(surf_table)
    #p = Period(days[0])
    #print(p.date, p.timestamp, p.height, p.wind, p.weather, p.temp)

    df = pd.DataFrame(columns=['timestamp', 'datetime', 'height',
                      'wind_steady', 'wind_gust', 'weather', 'temp'])
    for day in days:
        day_df = pd.DataFrame(data=Day(day).forecast, columns=[
                              'timestamp', 'datetime', 'height', 'wind_steady', 'wind_gust', 'weather', 'temp'])
        df = pd.concat([df, day_df], ignore_index=True)

    print(tabulate(df, headers=df.columns, tablefmt="fancy_grid", showindex=False))

    ideal = df['height'].isin(['Flat', '0ft', '0-1ft', '1-2ft']) & (df['datetime'].dt.hour > 6) & (df['wind_steady'] <= 10) & (
        df['wind_gust'] <= 15) & (df['weather'].isin(['Sunny', 'Clear', 'Cloudy', 'Mostly Cloudy'])) & (df['temp'] >= 5)

    surf = df.loc[ideal]

    if not surf.empty:
        print(tabulate(df.loc[ideal], headers=df.columns,
              tablefmt="fancy_grid", showindex=False))
    else:
        print("Not ideal")
