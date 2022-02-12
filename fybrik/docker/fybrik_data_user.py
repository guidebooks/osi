#!/usr/bin/python

import json
import pyarrow.flight as fl
import pandas as pd
import os
import sys

def get_data(endpoint, namespace):
    # Create a Flight client
    client = fl.connect(endpoint)
    print('Getting data for endpoint '+endpoint)

    # Prepare the request
    request = {
        "asset": namespace+"/paysim-csv",
        # To request specific columns add to the request a "columns" key with a list of column names
        # "columns": [...]
    }

    # Send request and fetch result as a pandas DataFrame
    info = client.get_flight_info(fl.FlightDescriptor.for_command(json.dumps(request)))
    reader: fl.FlightStreamReader = client.do_get(info.endpoints[0].ticket)
    df: pd.DataFrame = reader.read_pandas()
    print(df)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Not enough arguments provided')
    else:
        get_data(sys.argv[1], sys.argv[2])
