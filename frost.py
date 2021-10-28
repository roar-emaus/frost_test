
from dataclasses import dataclass

import csv
import requests


@dataclass
class Frost:
    client_id: str = None
    _base_url: str = "https://frost.met.no"
    _observations: str = "/observations"
    _elements: str = "/elements"
    _end_url: str = "/v0.jsonld"

    def get_client_id(self):
        with open("creds.txt", "r") as f:
            return f.readline().strip()

    def elements(self, names=None):
        endpoint = f"{self._base_url}{self._elements}{self._end_url}"
        parameters = dict(names=names)
        client_id = self.get_client_id()
        return dict(url=endpoint, params=parameters, auth=(client_id, ""))
    
    def available_timeseries(self, elements="mean(air_temperature PT1H)"):
        endpoint = f"{self._base_url}{self._observations}/availableTimeSeries{self._end_url}"
        parameters = dict(elements=elements)
        client_id = self.get_client_id()

        return dict(url=endpoint, params=parameters, auth=(client_id, ""))


frost = Frost()
print(frost.elements())
print(frost.available_timeseries(elements="mean(air_temperature PT1H)"))


result = requests.get(**frost.available_timeseries(elements="mean(air_temperature PT1H)"))

fieldnames = [
        "sourceId", "validFrom", "validTo", "timeOffset", "timeResolution",
        "timeSeriesId", "elementId", "unit", "performanceCategory", 
        "exposureCategory", "status"
        ]

with open("air_temperature_1h.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for d in result.json().get("data"):
        writer.writerow({field: d.get(field, '') for field in fieldnames})


