
import sys
from time import sleep
import argparse
import requests  # for calling api
import logging
import pandas as pd
import json
import os.path
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

def get_tsinfo_per_station(station_id):
    response_status = requests.get(f"https://geo.irceline.be/sos/api/v1/stations/{str(station_id)}?expanded=true")
    response = response_status.json()
    df = pd.DataFrame(response)
    df = pd.DataFrame(df.loc["timeseries", "properties"]).transpose().reset_index(names="timeseries_id")
    return df

def get_timeseries_meta(ts_id):
    response_status = requests.get(f"https://geo.irceline.be/sos/api/v1/timeseries/{ts_id}")
    response = response_status.json()
    try:
        os.makedirs("local_data/metadata")
    except Exception:
        pass
    fn = f"local_data/metadata/{ts_id}.json"
    with open(fn, 'w') as fp:
        json.dump(response, fp)
    # timeseries_meta = pd.json_normalize(response)  # 1 rij voor 1 timeseries, maar sommige timeseries hebben 26 kolommen sommige 27
    return response["parameters"]["phenomenon"]["id"]

def get_timeseries_datapoints(ts_id, station_id, date="2023-08-01"):
    date = date
    datefn = date.replace("-", "")
    timespan = f"?timespan=PT24H/{date}"
    #timespan = ""
    response_status = requests.get(f"https://geo.irceline.be/sos/api/v1/timeseries/{ts_id}/getData{timespan}")
    response = response_status.json()
    df = pd.DataFrame(response)
    df = pd.DataFrame(df['values'].values.tolist())
    try:
        os.makedirs(f"local_data/timeseries_data/{datefn}/{station_id}")
    except Exception:
        pass
    df.to_csv(f"local_data/timeseries_data/{datefn}/{station_id}/{ts_id}_data.txt", sep="\t", index=False)

stations_info = data_from_api(api_stations, norm=True)

# get timeseries ids for parameters of interest from station gent
station_gent = data_from_api(api_stations_gent, norm=False)
timeseries_gent = pd.DataFrame(station_gent.loc["timeseries", "properties"]).transpose().reset_index(names="timeseries_id")

# https://geo.irceline.be/sos/api/v1/timeseries/7087
# https://geo.irceline.be/sos/api/v1/timeseries/7087/getData?timespan=PT24H/2023-11-27

# get timeseries ids for per station
for station_id in stations_info["properties.id"]:
    which_ts_per_station = get_tsinfo_per_station(station_id)
    # get timeseries metadata for those timeseries available in station of interest
    for ts_id in which_ts_per_station.timeseries_id:
        phen_id = get_timeseries_meta(ts_id)
        print(phen_id)
        if phen_id=="5":  # pm10
            print(phen_id)
            # get timeseries datapoints
            dates = ["2023-08-01", "2023-08-02", "2023-08-03", "2023-08-04"]
            for date in dates:
                get_timeseries_datapoints(ts_id, station_id, date)
        else: continue