# Frost API collection

## Goal
Fetch time series data and store it into either a Shyft geodb DTSS or a regular
Shyft DTSS

## TODO:
- [ ] Check how many and how much of a time series to fetch at ones
- [ ] set up DTSS

## Files

### get_all_temperature_stations.py
First fetches all sensors with 1H resolution air temperature, then fetches
the metadata of those stations and stores it in a csv file (stations_air_temperature_1h.csv).
