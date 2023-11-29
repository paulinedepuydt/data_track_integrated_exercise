
import sys
from time import sleep
import argparse
import requests  # for calling api
import logging
import pandas as pd
import json
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.width', 180)
pd.set_option('display.max_columns', 20)

api_stations = f"https://geo.irceline.be/sos/api/v1/stations/?expanded=false"
api_stations_exp = "https://geo.irceline.be/sos/api/v1/stations/?expanded=true"
api_stations_gent = f"https://geo.irceline.be/sos/api/v1/stations/1207?expanded=true"

def data_from_api(url, norm):
    response_status = requests.get(url)
    response = response_status.json()
    if isinstance(response, dict): print(response)
    else: print(response[0])
    if norm: df = pd.json_normalize(response)
    else: df = pd.DataFrame(response)
    return df


stations = data_from_api(api_stations, norm=True)
stations_of_interest = stations[stations["properties.label"].str.contains("Gent|Antwerpen")]
station_ids_of_interest = stations_of_interest["properties.id"]

data_from_api(api_stations_exp, norm=False)

# TODO: met timespan parameter telkens de data opvragen van deze dag en wegschrijven, oorspronkelijk was wel de bedoeling om json weg te schrijven
# get timeseries ids for parameters of interest from station gent
station_gent = data_from_api(api_stations_gent, norm=False)
timeseries_gent = pd.DataFrame(station_gent.loc["timeseries", "properties"]).transpose().reset_index(names="timeseries_id")


# get timeseries metadata for those timeseries available in station of interest
def get_timeseries_meta(ts_id):
    response_status = requests.get(f"https://geo.irceline.be/sos/api/v1/timeseries/{ts_id}")
    response = response_status.json()
    fn = f"local_data/{ts_id}.json"
    with open('result.json', 'w') as fp:
        json.dump(sample, fp)
    response.dump(fn, response)
    timeseries_meta = pd.json_normalize(response)  # is 1 rij dus hiervan kan ik alle timeseries onder elkaar plakken uiteindelijk
    return timeseries_meta.columns

pd.DataFrame(list(map(get_timeseries_meta, timeseries_gent.timeseries_id)))  # sommige hebben statusIntervals => zou kunnen wegdoen maar dan kuis je al op...


"https://geo.irceline.be/sos/api/v1/timeseries/7087"
# get timeseries datapoints
timespan = "?timespan=PT24H/2023-11-27"
#timespan = ""
response_status = requests.get(f"https://geo.irceline.be/sos/api/v1/timeseries/{timeseries_gent.timeseries_id[0]}/getData{timespan}")
response = response_status.json()
df = pd.DataFrame(response)
df = pd.DataFrame(df['values'].values.tolist())
len(df)
df

