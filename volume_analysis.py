"""Analyze API volume and temporal coverage data."""

import requests
import json

BASE_URL = 'https://data.cityofchicago.org/resource/4g9f-3jbs.json'

# Fetch 5000 records from June 11, 2024
params = {
    "$select": "time,segment_id,speed,length,hour,day_of_week,month",
    "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-12T00:00:00'",
    "$limit": 5000
}
r = requests.get(BASE_URL, params=params, timeout=30)
data = r.json()

# Analyze dates
years = set()
months = set()
for rec in data:
    t = rec.get("time", "")
    if t:
        years.add(t[:4])
        if len(t) >= 7:
            months.add(t[:7])

print("Years in sample:", sorted(years))
print("Months in sample:", sorted(months))
print("Total records:", len(data))

# Speed quality
valid = 0
invalid = 0
for rec in data:
    s = rec.get("speed", "")
    if s == "-1" or s == -1:
        invalid += 1
    else:
        valid += 1
print(f"Valid speed: {valid}, Invalid (=-1): {invalid}")
print(f"Invalid percentage: {invalid/len(data)*100:.1f}%")

# Hour distribution
hours = set()
for rec in data:
    h = rec.get("hour", "")
    if h:
        hours.add(int(h))
print("Hours observed:", sorted(hours))
print("Number of unique hours:", len(hours))

# Segment IDs
segs = set()
for rec in data:
    s = rec.get("segment_id", "")
    if s:
        segs.add(s)
print("Unique segments:", len(segs))

# Length values
lengths = set()
for rec in data:
    l = rec.get("length", "")
    if l:
        lengths.add(l)
print("Length values observed:", lengths)
PYEOF