import csv
import calendar
from datetime import datetime, time

import numpy as np
import matplotlib.pyplot as plot, matplotlib.dates as dates

plot.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%S'))
plot.gca().xaxis.set_major_locator(dates.HourLocator())

with open("occupancy2.csv", "r") as f:
	reader = csv.reader(f)

	per_day = {day_abbr: [] for day_abbr in calendar.day_abbr}
	for t_occ in [(datetime.fromtimestamp(float(t)), int(occ)) for t, occ in reader]:
		day_abbr = calendar.day_abbr[t_occ[0].weekday()]
		per_day[day_abbr].append(t_occ)

for day_abbr, t_occ in per_day.items():
	if t_occ:
		try:
			times, occ = zip(*((t, occ) for t, occ in t_occ if occ > 1 and t.hour >= 6 and t.hour <= 22))
		except ValueError:
			continue
		
		t = [dates.date2num(datetime(1, 1, 1, hour=dt.hour, minute=dt.minute)) for dt in times]
		plot.plot(t, occ, label=day_abbr) # s=12


six_thirty_am = dates.date2num(datetime(1, 1, 1, hour=6, minute=30))
ten_thirty_pm = dates.date2num(datetime(1, 1, 1, hour=22, minute=30))
eight_am = dates.date2num(datetime(1, 1, 1, hour=8, minute=0))
nine_pm = dates.date2num(datetime(1, 1, 1, hour=21, minute=0))

plot.axvline(x=six_thirty_am, color="black", linestyle="--")
plot.axvline(x=ten_thirty_pm, color="black", linestyle="--")

"""
if "Sat" in per_day or "Sun" in per_day:
	if "Sun" in per_day:
		plot.axvline(x=nine_pm, color="black", linestyle="--")

	plot.axvline(x=eight_am, color="black", linestyle="--")
"""

plot.gcf().autofmt_xdate()

plot.ylabel("Gym occupancy (%)")
plot.xlabel("Time (HH:MM)")
plot.grid()
plot.legend()
plot.show()
