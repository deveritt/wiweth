from wiweth import settings
from wiweth.utils import make_request
import datetime
from datetime import date


class MapQuestApi:
    """
    This class is extensible for other mapquest utilities, here I'm only going to provide the method for
    converting a location string to latitude and longitude (and in an array as we have no GIS).
    """
    def __init__(self):

        self.url = getattr(settings, 'MAPQUEST_URL','http://open.mapquestapi.com/geocoding/v1/batch')
        self.api_key = getattr(settings, 'MAPQUEST_KEY', 'YVRoMnYml4JAht1mKnerUWFPSxoO7NRj')

    def location_to_lat_long(self, location:str ='Cape Town')->list:

        response = make_request(
            "{}?key={}&location={}".format(self.url, self.api_key, location),
            {}
        )

        result = []

        if (
            'results' in response and
            len(response['results']) > 0 and
            'locations' in response['results'][0] and
            len(response['results'][0]['locations']) > 0 and
            'latLng' in response['results'][0]['locations'][0] and
            'lat' in response['results'][0]['locations'][0]['latLng'] and
            'lng' in response['results'][0]['locations'][0]['latLng']

        ):
            return [
                response['results'][0]['locations'][0]['latLng']['lat'],
                response['results'][0]['locations'][0]['latLng']['lng']
            ]

        else:
            raise ValueError("Unable to determine co-ordinates for {}".format(location))


class DarkSkyApi:
    """
    This API is to get weather information from darksky.
    """
    def __init__(self, lat:float, long:float):

        self.url = getattr(settings, 'DARKSKY_URL', 'https://dark-sky.p.rapidapi.com/')
        self.headers = getattr(
            settings,
            'DARKSKY_KEYS',
            {
                'x-rapidapi-host': "dark-sky.p.rapidapi.com",
                'x-rapidapi-key': "70ca552227msh7bd56e705153d45p19c40djsnde287025c04b"
            }
        )
        self.lat = lat
        self.long = long


    def get_historical_data(self, day: date)->dict:

        epoch = int(datetime.datetime.combine(day, datetime.datetime.min.time()).timestamp())
        response = make_request(
            "{}{},{},{}".format(self.url, self.lat, self.long, epoch),
            self.headers
        )

        if 'daily' in response and 'data'in response['daily'] and len(response['daily']['data']) > 0:
            return response['daily']['data'][0]
        else:
            raise ValueError(
                "Unable to get weather statistics for {}, {} for {} from DarkSky.".format(
                    self.lat,
                    self.long,
                    day
                )
            )

    def get_period_data(self, start_day: date, end_day:date)->dict:

        end_date = end_day if end_day < date.today() else date.today() - datetime.timedelta(days=1)
        if start_day > end_day:
            raise ValueError("Cannot weather collect data in the future.")

        result = {
            'temperature': {
                'min': 1000,
                'max': 0,
                'average': 0,
                'median': 0
            },
            'humidity': {
                'min': 1000,
                'max': 0,
                'average': 0,
                'median': 0
            }
        }
        total_temperature = 0
        total_humidity = 0

        count = 0
        get_day = start_day

        while get_day <= end_date:

            data = self.get_historical_data(get_day)

            if data['temperatureMin'] < result['temperature']['min']:
                result['temperature']['min'] = data['temperatureMin']
            if data['temperatureMax'] > result['temperature']['max']:
                result['temperature']['max'] = data['temperatureMax']
            total_temperature += (data['temperatureMin'] + data['temperatureMax']) / 2

            if data['humidity'] < result['humidity']['min']:
                result['humidity']['min'] = data['humidity']
            if data['humidity'] > result['humidity']['max']:
                result['humidity']['max'] = data['humidity']
            total_humidity += data['humidity']

            count += 1
            get_day = get_day + datetime.timedelta(days=1)
            print(repr(get_day))

        result['temperature']['average'] = total_temperature / count
        result['temperature']['median'] = (result['temperature']['min'] + result['temperature']['max']) / 2
        result['humidity']['average'] = total_temperature / count
        result['humidity']['median'] = (result['humidity']['min'] + result['humidity']['max']) / 2

        return result
