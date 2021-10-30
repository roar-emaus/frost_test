
import csv
import requests
import shyft.time_series as sts


sources = {}

with open("creds.txt", "r") as f:
    client_id = f.readline().strip()

endpoint = "https://frost.met.no/observations/availableTimeSeries/v0.jsonld"
parameters = dict(elements="mean(air_temperature PT1H)")
result = requests.get(endpoint, parameters, auth=(client_id, ''))

for d in result.json().get("data", []):
    source_id = d.get("sourceId").split(":")[0]
    valid_from = d.get("validFrom", None)
    valid_to = d.get("validTo", None)
    time_resolution = d.get("timeResolution", None)

    if source_id not in sources:
        sources[source_id] = dict(
                valid_from=valid_from,
                valid_to=valid_to,
                )
    else:
        old_valid_from = sources[source_id].get("valid_from")
        old_valid_to = sources[source_id].get("valid_to")
        if old_valid_from and sts.time(old_valid_from) < sts.time(valid_from):
            sources[source_id]["valid_from"] = valid_from

        if old_valid_to:
            if valid_to:
                if sts.time(old_valid_to) < sts.time(valid_to):
                    sources[source_id]["valid_to"] = valid_to
            else:
                sources[source_id]["valid_to"] = ""
            

endpoint = "https://frost.met.no/sources/v0.jsonld"
parameters = dict(ids=','.join(s.split(":")[0] for s in list(sources.keys())))
auth=(client_id, '')

result = requests.get(endpoint, parameters, auth=auth)

for d in result.json().get("data", []):
    source_id = d.get("id")
    name = d.get("shortName")
    geometry = d.get("geometry")
    longitude, latitude = geometry.get("coordinates")
    masl = d.get("masl")
    county = d.get("county")
    municipality = d.get("municipality")
    sensor_valid_from = d.get("validFrom")

    sources[source_id].update(dict(
        name=name, latitude=latitude, longitude=longitude, masl=masl,
        county=county, municipality=municipality,
        sensor_valid_from=sensor_valid_from,
        ))


fieldnames = [k for k in list(sources.values())[0]]
fieldnames.insert(0, "source_id")

with open("stations_air_temperature_1h.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for s_id, source in sources.items():
        source.update({"source_id": s_id})
        writer.writerow(source)

