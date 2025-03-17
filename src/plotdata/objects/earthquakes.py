import sys
import os

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import requests
from datetime import datetime
from matplotlib import pyplot as plt
from utils import draw_box, calculate_distance
from constants import volcanoes


class Earthquake():
    def __init__(self, volcano, start_date, end_date = None, distance_km = 20, distance_deg = None, magnitude = 3):
        # Constants
        self.API_ENDPOINT = "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
        self.PARAMS = {
            "eventtype": "earthquake",
            "orderby": "time",
        }
        self.volcano = volcanoes[volcano]

        self.start_date = datetime.strptime(start_date,'%Y%m%d') if isinstance(start_date, str) else start_date
        self.end_date = datetime.today() if not end_date else datetime.strptime(end_date, '%Y%m%d') if isinstance(end_date, str) else end_date
        self.magnitude = magnitude

        self.region = draw_box(self.volcano['lat'], self.volcano['lon'], distance_km, distance_deg)
        self.get_earthquake_data()


    def construct_url(self, max_lat, min_lat, max_lon, min_lon):
        params = self.PARAMS.copy()
        params["starttime"] = self.start_date.isoformat()
        params["endtime"] = self.end_date.isoformat()
        params["maxlatitude"] = max_lat
        params["minlatitude"] = min_lat
        params["maxlongitude"] = max_lon
        params["minlongitude"] = min_lon
        params["minmagnitude"] = self.magnitude
        return f"{self.API_ENDPOINT}?{ '&'.join([f'{k}={v}' for k,v in params.items()])}"


    def get_earthquake_data(self):
        min_lon, max_lon, min_lat, max_lat = self.region
        url = self.construct_url(max_lat, min_lat, max_lon, min_lon)

        print("#" * 50)
        print("USGS database")
        print("#" * 50)
        print()

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            features = data['features']

            earthquakes = {
                "date" : [],
                "lalo" : [],
                "magnitude" : [],
                "moment" : []
            }
            for feature in features:
                timestamp = feature['properties']['time'] / 1000
                date_time = datetime.utcfromtimestamp(timestamp).date()

                latitude = feature['geometry']['coordinates'][1]
                longitude = feature['geometry']['coordinates'][0]

                earthquakes["date"].append(date_time)
                earthquakes["lalo"].append((latitude, longitude))
                earthquakes["magnitude"].append(float(feature['properties']['mag']))


            self.earthquakes = earthquakes

        except requests.exceptions.RequestException as e:
            msg = f"Error fetching data: {e}"

            raise Exception(msg)


    def print(self):
        for i in range(len(self.earthquakes['date'])):
            print(self.earthquakes['date'][i])
            print(self.earthquakes['magnitude'][i])
            print(self.earthquakes['lalo'][i])
            print(f"Distance from {self.volcano}: {calculate_distance(self.earthquakes['lalo'][i][0], self.earthquakes['lalo'][i][1], self.volcano['lat'], self.volcano['lon'])} km\n")


    def plot(self):
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        self.plot_by_date(ax1)
        self.plot_by_distance(ax2)

        plt.show()


    def plot_by_date(self, ax):
        # Plot EQs
        for i in range(len(self.earthquakes['date'])):
            ax.plot([self.earthquakes['date'][i], self.earthquakes['date'][i]], [self.earthquakes['magnitude'][i], 0], 'k-')

        ax.scatter(self.earthquakes['date'], self.earthquakes['magnitude'], c='black', marker='o')
        ax.set_xlabel('Date')
        ax.set_ylabel('Magnitude')
        ax.set_title('Earthquake Magnitudes Over Time')
        ax.set_xlim([self.start_date.date(), self.end_date.date()])
        ax.set_ylim([0, 10])


    def plot_by_distance(self, ax):
        # Plot EQs
        dist = []
        for i in range(len(self.earthquakes['date'])):
            dist.append(calculate_distance(self.earthquakes['lalo'][i][0], self.earthquakes['lalo'][i][1], self.volcano['lat'], self.volcano['lon']))
            ax.plot([dist[i], dist[i]], [self.earthquakes['magnitude'][i], 0], 'k-')

        ax.set_xlim([0, max(dist)+ (max(dist) * 0.05)])
        ax.set_ylim([0, 10])

        ax.scatter(dist, self.earthquakes['magnitude'], c='black', marker='o')

        ax.set_xlabel('Distance in KM')
        ax.set_ylabel('Magnitude')
        ax.set_title('Earthquake Magnitudes from Volcano')