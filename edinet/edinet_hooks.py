import codecs
import csv
import json
from datetime import datetime
from math import radians, sin, asin, sqrt, cos

import flask
from flask import current_app as app

from base_hooks import BaseHook

class MeasuresHooks(BaseHook):
    def __init__(self, measures_resources):
        self.resources = measures_resources
    def measures_insert(self):
        def measures_hook(resource_name, documents):
            if resource_name in self.resources:
                for doc in documents:
                    # Check each measure has its readings:
                    readings_types = set([x['type'] for x in doc['readings']])
                    measures_types = set([x['type'] for x in doc['measurements']])
                    if measures_types.difference(readings_types):
                        flask.abort(404, description="Types on readings are not 1-n related")

                    # check if the readings are exactly the same or create a new one
                    readings = {}
                    readings_count = 0
                    for r in doc['readings']:
                        x = app.data.driver.db['readings'].find_one(r)
                        if x:
                            readings[x['type']] = x['_id']
                        else:
                            readings_count +=1
                            r.update({"_created": datetime.now(), "_updated": datetime.now()})
                            x = app.data.driver.db['readings'].insert_one(r)
                            readings[r['type']] = x.inserted_id
                    # insert the measures, add the common information and the relation with the reading document
                    # generate a dic for all measures
                    global_dic = {"companyId": doc['companyId'], "deviceId": doc['deviceId']}
                    measures = []
                    for m in doc['measurements']:
                        reading_id = readings[m['type']]
                        m.update({**global_dic, "reading": reading_id, "_created": datetime.now(),
                                  "_updated": datetime.now()})
                        measures.append(m)
                    app.data.driver.db['{}_measurements'.format(resource_name)].insert_many(measures)
                    response = {'measures_uploaded': len(measures), 'readings_uploaded': readings_count}
                    flask.abort(flask.Response(json.dumps(response)))
        return measures_hook
    @staticmethod
    def set_hooks(app):
        measures_hoock = MeasuresHooks(app.config["MEASURES_RESOURCES"])
        app.on_insert += measures_hoock.measures_insert()


class WeatherStationHooks(BaseHook):
    def __init__(self, geo_file, default_lat, default_long, default_alt):
        self.GEOLOC_PATH = geo_file
        self.GEOLOC_DEFAULT_LATITUDE = default_lat
        self.GEOLOC_DEFAULT_LONGITUDE = default_long
        self.GEOLOC_DEFAULT_ALTITUDE = default_alt

    def _haversine(self, lon1, lat1, lon2, lat2):
        """ Calculate the great circle distance between two points on the earth (specified in decimal degrees) """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def _dms2dd(self, degrees, minutes, seconds, direction):
        """ dms to dd"""
        dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60);
        if direction == 'S' or direction == 'W':
            dd *= -1
        return dd

    def _get_lan_long_alt_from_file(self, postalCode, countryCode):
        file_postalCode = self.GEOLOC_PATH
        with codecs.open(file_postalCode, 'r', 'utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                if postalCode == str(row[0]) and countryCode == row[4]:
                    contract_lat = float(row[1])
                    contract_long = float(row[2])
                    contract_altitude = float(row[3])
                    break
            try:
                contract_lat
                contract_long
                contract_altitude
            except:
                contract_lat = self.GEOLOC_DEFAULT_LATITUDE
                contract_long = self.GEOLOC_DEFAULT_LONGITUDE
                contract_altitude = self.GEOLOC_DEFAULT_ALTITUDE
        return contract_lat, contract_long, contract_altitude

    def _calculate_closest_weather_station(self, postalCode, countryCode):
        # find the gps position of the given info
        contract_lat, contract_long, contract_altitude = self._get_lan_long_alt_from_file(postalCode, countryCode)
        print(contract_lat, contract_long, contract_altitude)
        """ look for the closer weather station in a loop of weatherStation of mongo """
        query = {}
        stations = app.data.driver.db['weather_stations'].find(query)
        dist = 1e19
        stationId="unknown"
        for station in stations:
            if 'latitude' in station and 'longitude' in station and station['latitude'] and station['longitude']:
                try:
                    lat_dd = float(station['latitude'])
                    long_dd = float(station['longitude'])
                except Exception:
                    print('error with station: {}'.format(station['stationId']))
                    continue

                new_dist = self._haversine(contract_long, contract_lat, long_dd, lat_dd)

                if dist > new_dist:
                    dist = new_dist
                    stationId = station['stationId']

        return stationId, dist

    def _return_station_distance_from_doc(self, doc):
        # buscar station mes propera
        stationId = 'Unknown'
        distance = None
        if 'location' in doc:
            if 'postalCode' in doc['location'] and 'countryCode' in doc['location']:
                stationId, distance = self._calculate_closest_weather_station(doc['location']['postalCode'],
                                                                              doc['location']['countryCode'])
        return stationId, distance

    def add_weather_station(self):
        def add_weather_station_hook(documents):
            for doc in documents:
                stationId, distance = self._return_station_distance_from_doc(doc)
                doc['stationId'] = stationId
                doc['distance'] = distance
        return add_weather_station_hook

    def update_weather_station(self):
        def update_weather_station_hook(updates, original):
            original.update(updates)
            stationId, distance = self._return_station_distance_from_doc(original)
            updates['stationId'] = stationId
            updates['distance'] = distance
        return update_weather_station_hook

    @staticmethod
    def set_hooks(app):
        weather_station_hook = WeatherStationHooks(app.config['POSTAL_CODE_FILE'], app.config['DEFAULT_LATITUDE'], app.config['DEFAULT_LONGITUDE'], app.config['DEFAULT_ALTITUDE'])
        app.on_insert_modelling_units += weather_station_hook.add_weather_station()
        app.on_update_modelling_units += weather_station_hook.update_weather_station()

class BuildingHourlyHook(BaseHook):
    def get_resource(self):
        def hourly_data_hook_building(response):
            for resource in response['_items']:
                modelling_units = resource['modellingUnits'] if 'modellingUnits' in resource else []
                if not modelling_units:
                    reporting_unit_doc = app.data.driver.db['reporting_units'].find_one({'buildingId': resource['buildingId']})
                    if reporting_unit_doc and 'modelling_Units' in reporting_unit_doc:
                        modelling_units = reporting_unit_doc['modelling_Units']
                if not modelling_units:
                    resource['hourlyData'] = False
                    continue
                hourly = []
                for mu in modelling_units:
                    baseline_doc = app.data.driver.db['baselines'].find_one({'modellingUnitId':mu})
                    if baseline_doc:
                        hourly.append(len(baseline_doc['timestamps']) > 0 if 'timestamps' in baseline_doc else False)
                    else:
                        hourly.append(False)
                response['hourlyData'] = any(hourly)

        return hourly_data_hook_building

    def get_item(self):
        def hourly_data_hook_building(response):
            modelling_units = response['modellingUnits'] if 'modellingUnits' in response else []
            if not modelling_units:
                reporting_unit_doc = app.data.driver.db['reporting_units'].find_one({'buildingId': response['buildingId']})
                if reporting_unit_doc and 'modelling_Units' in reporting_unit_doc:
                    modelling_units = reporting_unit_doc['modelling_Units']
            if not modelling_units:
                response['hourlyData'] = False
                return
            hourly = []
            for mu in modelling_units:
                baseline_doc = app.data.driver.db['baselines'].find_one({'modellingUnitId':mu})
                if baseline_doc:
                    hourly.append(len(baseline_doc['timestamps']) > 0 if 'timestamps' in baseline_doc else False)
                else:
                    hourly.append(False)
            response['hourlyData'] = any(hourly)

        return hourly_data_hook_building

    @staticmethod
    def set_hooks(app):
        b_hook = BuildingHourlyHook()
        app.on_fetched_resource_buildings += b_hook.get_resource()
        app.on_fetched_item_buildings += b_hook.get_item()