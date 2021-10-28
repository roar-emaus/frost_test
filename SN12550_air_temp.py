
import requests
import matplotlib.pyplot as plt


endpoint = "https://frost.met.no/observations/v0.jsonld"
parameters = dict(
        sources="SN12550:0",
        referencetime="1982-01-01/1993-01-26",
        elements="mean(air_temperature PT1H)",
        timeoffsets="PT0H",
        timeresolutions="PT1H",
        timeseriesids="0",
        performancecategories="C",
        exposurecategories="2",
        levels="2.0"
        )

with open("creds.txt", "r") as f:
    client_id = f.readline().strip()

times = [f"{t}-01-01" for t in range(1982, 2022)]

timestamps = []
values = []
for t0, t1 in zip(times[:-1], times[1:]):
    parameters["referencetime"] = f"{t0}/{t1}"
    print(parameters["referencetime"] )
    result = requests.get(endpoint, parameters, auth=(client_id, ''))
    print(result)
    for d in result.json().get("data", []):
        timestamps.append(d["referenceTime"])
        values.append(d["observations"][0]["value"])

with open("air_temp_test.txt", "w") as f:
    for t, v in zip(timestamps, values):
        f.write(f"{t},{v}\n")
#print(result)
#
#with open("air_temp_test.txt", "w") as f:
#    for d in result.json()["data"]:
#        f.write(f'{d["observations"][0]["value"]}\n')
