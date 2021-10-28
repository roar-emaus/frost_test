from datetime import datetime as dt
import shyft.time_series as sts
import matplotlib
import numpy as np
import matplotlib.pyplot as plt


timestamps, values = [], []
with open("air_temp_test.txt", "r") as f:

    for line in f.readlines():
        timestamp, value = line.split(",")
        timestamp = timestamp.split(":")[0]
        t = dt.strptime(timestamp, "%Y-%m-%dT%H")
        v = float(value.strip())
        timestamps.append(t)
        values.append(v)


utc = sts.Calendar()
ta = sts.TimeAxis([t.timestamp() for t in timestamps], t_end=t.timestamp()+1)
p = ta.total_period()
ta_mean = sts.TimeAxis(p.start, utc.YEAR, p.diff_units(utc, utc.YEAR))
ts = sts.TimeSeries(ta, values, sts.point_interpretation_policy.POINT_AVERAGE_VALUE)
ts_mean = ts.average(ta_mean)

ts_dates = matplotlib.dates.date2num([dt.utcfromtimestamp(p.start) for p in ta])
ts_mean_dates = matplotlib.dates.date2num([dt.utcfromtimestamp(p.start) for p in ta_mean])
x = np.array(range(len(ts.v.to_numpy())))
y = ts.v.to_numpy()
z = np.polyfit(x, y, 1)


plt.plot_date(ts_dates, ts.v.to_numpy(), linestyle='-', marker=None)
plt.plot_date([ts_dates[0], ts_dates[-1]], z, linestyle='-', label=f"t0: {z[0]:.1f}, t1: {z[-1]:.1f}")
plt.legend()
plt.show()
