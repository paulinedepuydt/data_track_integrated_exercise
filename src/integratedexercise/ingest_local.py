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

#api_url = "https://geo.irceline.be/sos//api/v1/stations?offset=4&limit=2"
api_stations = "https://geo.irceline.be/sos/api/v1/stations/?expanded=false"
api_stations_exp = "https://geo.irceline.be/sos/api/v1/stations/?expanded=true"

def data_from_api(url, norm):
    response = requests.get(url)
    responsej = response.json()
    print(response)
    print(responsej[100])
    if norm: df = pd.json_normalize(responsej)
    else: df = pd.DataFrame(responsej)
    print(df)

#data_from_api(api_stations, norm=True)
#data_from_api(api_stations_exp, norm=False)

# TODO: met timespan parameter telkens de data opvragen van deze dag en wegschrijven, oorspronkelijk was wel de bedoeling om json weg te schrijven

response = requests.get("https://geo.irceline.be/sos/api/v1/timeseries/10987/getData")
responsej = response.json()
print(responsej)
df = pd.DataFrame(responsej)
df = pd.DataFrame(df['values'].values.tolist())
print(df.head(20))
