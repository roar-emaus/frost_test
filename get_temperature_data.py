
import csv
import requests
import shyft.time_series as sts
from shyft.time_series import point_interpretation_policy as p_fx


with open("creds.txt", "r") as f:
    CLIENT_ID = f.readline().strip()


def get_parameters(sensor_id: str, t_0: str, t_1: str):
    endpoint = "https://frost.met.no/observations/v0.jsonld"
    parameters = dict(
            sources=f"{sensor_id}:0",
            referencetime=f"{t_0}/{t_1}",
            elements="mean(air_temperature PT1H)",
            timeoffsets="PT0H",
            timeresolutions="PT1H",
            )
    
    return dict(url=endpoint, params=parameters, auth=(CLIENT_ID, ""))


def store_ts(sensor_id: str, timepoints: list, values: list):
    client = sts.DtsClient("localhost:20001")
    timepoints = list(map(sts.time, timepoints))
    ta = sts.TimeAxis(timepoints, t_end=timepoints[-1] + 3600)
    ts = sts.TimeSeries(ta, values, p_fx.POINT_AVERAGE_VALUE)
    store_ts = sts.TimeSeries(
            ts_id=f"shyft://frost/{sensor_id}_mean_air_temperature",
            bts=ts
            )
    client.store_ts(
            sts.TsVector([store_ts]), overwrite_on_write=False,
            cache_on_write=True
            )


def parse_results(results):
    data = results.json().get("data", [])
    timepoints = []
    values = []
    for d in data:
        timepoints.append(d["referenceTime"])
        values.append(d["observations"][0]["value"])

    return timepoints, values


def request_data(sensor_id: str, valid_from: str, valid_to: str):
    utc = sts.Calendar()
    if not valid_to:
        c = utc.calendar_units(sts.utctime_now())
        valid_to = f"{c.year}-{c.month:02d}-{c.day:02d}T{c.hour:02d}:00:00Z"
    
    valid_from_calendar = utc.calendar_units(sts.time(valid_from))
    valid_to_calendar = utc.calendar_units(sts.time(valid_to))

    year_range = list(range(valid_from_calendar.year, valid_to_calendar.year + 2))
    print(sensor_id)
    for year_from, year_to in zip(year_range[:-1], year_range[1:]):
        t_0 = f"{year_from}-01-01T00:00:00Z" 
        t_1 = f"{year_to}-01-01T00:00:00Z" 
        print(year_from, year_to)
        request_params = get_parameters(sensor_id, t_0=t_0, t_1=t_1)
        result = requests.get(**request_params)
        print(result)
        if result.status_code == 200:
            timepoints, values = parse_results(result) 
            store_ts(sensor_id, timepoints, values)
        else:
            print(result.json())


def get_sensors_metadata():
    sensor_metadata = {}
    with open("stations_air_temperature_1h.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor_metadata[row.get("source_id")] = (
                    row.get("valid_from"), row.get("valid_to")
                    )
    return sensor_metadata
        


sensors_metadata = get_sensors_metadata()
for source_id, source_meta in sensors_metadata.items():
    request_data(source_id, *source_meta)

"""
utc = sts.Calendar()
ta = sts.TimeAxis([sts.min_utctime, sts.max_utctime])
ts = sts.TimeSeries(ta,  1, sts.point_interpretation_policy.POINT_AVERAGE_VALUE)
print(ts.time_axis)
i_tsv = sts.TsVector([sts.TimeSeries(ts_id="shyft://data/test_ts", bts=ts)])

client = sts.DtsClient("localhost:20001")
client.store_ts(tsv=i_tsv, overwrite_on_write=True, cache_on_write=True)
"""
