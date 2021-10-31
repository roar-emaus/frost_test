
import csv
from pathlib import Path
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import shyft.time_series as sts



def get_metadata():
    sensor_metadata = {}
    with open("stations_air_temperature_1h.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor_metadata[row.get("source_id")] = dict(
                    longitude=row.get("longitude"),
                    latitude=row.get("latitude"),
                    masl=row.get("masl"),
                    name=row.get("name"),
                    municipality=row.get("municipality"),
                    )
    return sensor_metadata


def create_ts_id(sensor_id: str):
    return f"shyft://frost/{sensor_id}_mean_air_temperature"


def to_datetime(ts: sts.TimeSeries):
    dates = mdates.date2num([dt.utcfromtimestamp(int(p.start)) for p in ts.time_axis]) 
    return dates


def plot_temperature():

    c = sts.DtsClient("localhost:20001")
    plot_store_path = Path("data/outplot/")

    for sensor_id, metadata in get_metadata().items():
        fig, ax = plt.subplots(figsize=(19.2,10.8))
        ts = c.evaluate(
                sts.TsVector([sts.TimeSeries(create_ts_id(sensor_id))]),
                sts.UtcPeriod(sts.min_utctime, sts.max_utctime)
                )[0]
        dates = to_datetime(ts)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%dT%H'))
        ax.plot(dates, ts.v.to_numpy())
        try:
            lat = float(metadata.get('latitude'))
            lon = float(metadata.get('longitude'))
        except ValueError:
            lat = 0
            lon = 0

        ax.set_title(
                f"{metadata.get('name')} ({metadata.get('masl')} masl) "
                f" lat: {lat:.2f} lon: {lon:.2f}"
                )
        ax.minorticks_on()
        ax.set_ylabel("C")
        ax.grid(b=True, which="both", axis="y", linestyle="--")
        plt.gcf().autofmt_xdate()
        fig.savefig(plot_store_path/f"{sensor_id}_temperature.png")
        plt.close(fig)


plot_temperature()   

