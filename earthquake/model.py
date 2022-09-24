import json
import os
from datetime import datetime, timedelta, timezone

import requests
from plotly import offline
from plotly.graph_objs import Layout


class Model:
    """
    Model for the Earthquake App.

    Uses data from USGS website in GeoJson format for last day, week, and month.
    """

    def __init__(self):
        self.timeframes = {
            "DAY": {
                "url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.geojson",
                "json": "data/earthquake_data_day_M1.json",
                "html": "data/earthquake_plot_day_M1.html",
            },
            "WEEK": {
                "url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.geojson",
                "json": "data/earthquake_data_week_M1.json",
                "html": "data/earthquake_plot_week_M1.html",
            },
            "MONTH": {
                "url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_month.geojson",
                "json": "data/earthquake_data_month_M1.json",
                "html": "data/earthquake_plot_month_M1.html",
            },
        }
        self.directory_name = os.path.dirname(__file__)

    def get_all_earthquake_data(self):
        for timeframe in self.timeframes:
            self._save_content(self._get_content(timeframe), timeframe)

    def _get_content(self, timeframe):
        response = requests.get(self.timeframes[timeframe]["url"])
        return response.content

    def _save_content(self, content, timeframe):
        with open(
            os.path.join(self.directory_name, self.timeframes[timeframe]["json"]), "wb"
        ) as f:
            f.write(content)

    def create_all_earthquake_plots(self):
        for timeframe in self.timeframes:
            self._create_earthquake_plot(timeframe)

    def _create_earthquake_plot(self, timeframe):
        content = self._read_content(timeframe)
        earthquakes = content["features"]

        magnitudes = []
        longitudes, latitudes = [], []
        hover_texts = []

        for earthquake in earthquakes:
            magnitudes.append(earthquake["properties"]["mag"])
            longitudes.append(earthquake["geometry"]["coordinates"][0])
            latitudes.append(earthquake["geometry"]["coordinates"][1])
            earthquake_time_utc = datetime.fromtimestamp(
                earthquake["properties"]["time"] / 1e3,
                timezone(timedelta(hours=0)),
            )
            hover_text = (
                earthquake["properties"]["title"]
                + " "
                + earthquake_time_utc.strftime("%x %X %Z")
            )
            hover_texts.append(hover_text)

        data = [
            {
                "type": "scattergeo",
                "lon": longitudes,
                "lat": latitudes,
                "text": hover_texts,
                "marker": {
                    "size": [5 * magnitude for magnitude in magnitudes],
                    "color": magnitudes,
                    "colorscale": "Jet",
                    "reversescale": False,
                    "colorbar": {"title": "Magnitude"},
                },
            }
        ]
        time_data_generated_utc = datetime.fromtimestamp(
            content["metadata"]["generated"] / 1e3,
            timezone(timedelta(hours=0)),
        )
        my_title = (
            content["metadata"]["title"]
            + " generated "
            + time_data_generated_utc.strftime("%x %X %Z")
        )
        my_layout = Layout(title=my_title)

        figure = {"data": data, "layout": my_layout}
        offline.plot(
            figure,
            filename=os.path.join(
                self.directory_name, self.timeframes[timeframe]["html"]
            ),
            auto_open=False,
        )

    def _read_content(self, timeframe):
        with open(
            os.path.join(self.directory_name, self.timeframes[timeframe]["json"])
        ) as f:
            content = json.load(f)

        return content

    def get_plot_filename(self, timeframe):
        return os.path.join(self.directory_name, self.timeframes[timeframe]["html"])
