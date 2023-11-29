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
api_stations_gent = f"https://geo.irceline.be/sos/api/v1/stations/1207"

def data_from_api(url, norm):
    response = requests.get(url)
    responsej = response.json()
    print(responsej[0])
    if norm: df = pd.json_normalize(responsej)
    else: df = pd.DataFrame(responsej)
    return df


stations = data_from_api(api_stations, norm=True)
stations_of_interest = stations[stations["properties.label"].str.contains("Gent|Antwerpen")]
station_ids_of_interest = stations_of_interest["properties.id"]

data_from_api(api_stations_exp, norm=False)

# TODO: met timespan parameter telkens de data opvragen van deze dag en wegschrijven, oorspronkelijk was wel de bedoeling om json weg te schrijven

# get timeseries ids for parameters of intereset from station gent
data_from_api(api_stations_gent, norm=False)


response = requests.get("https://geo.irceline.be/sos/api/v1/timeseries/10987/?category=71")
responsej = response.json()
print(responsej)
df = pd.DataFrame(responsej)
df = pd.DataFrame(df['values'].values.tolist())
print(df.head(20))
