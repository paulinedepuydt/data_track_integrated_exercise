import sys
from time import sleep

import argparse
import requests  # for calling api
import logging
import pandas as pd

#api_url = "https://geo.irceline.be/sos//api/v1/stations?offset=4&limit=2"
api_url = "https://geo.irceline.be/sos/api/v1/stations/?expanded=false"
response = requests.get(api_url)
responsej = response.json()
print("OK")
print(response)
df = pd.DataFrame(responsej)
print(df)