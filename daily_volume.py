"""Daily volume investigation for Chicago Traffic Tracker SODA2 API.

Runs COUNT queries for specified date ranges and calculates daily statistics.
Does NOT download all rows - only counts.
"""

import requests
import json
import os
from datetime import datetime, timedelta

BASE_URL = 'https://data.cityofchicago.org/resource/4g9f-3jbs.json'

# Date ranges to investigate (each is a full day from 00:00:00 to next day 00:00:00)
dates = [
    "2024-06-11",
    "2024-06-12",
    "2024-06-13",
    "2024-06-14",
    "2024-06-15",
    "2024-06-16",
    "2024-06-17"
]

# Build date ranges
date_ranges = []
for i, d in enumerate(dates):
    next_date = datetime.strptime(dates[i], "%Y-%m-%d") + timedelta(days=1)
    next_str = next_date.strftime("%Y-%m-%dT%H:%M:%S")
    date_ranges.append((d, f"'{d}T00:00:00'", next_str))

print("=" * 60)
print("DAILY VOLUME INVESTIGATION")
print("=" * 60)

results = []

for i, (date_str, date_start, date_end) in enumerate(date_ranges):
    print(f"\n--- Date {i+1}: {date_str} ---")
    
    # Query 1: Total count
    params_total = {
        "$select": "count(*)",
        "$where": f"time >= {date_start} AND time < {date_end}",
        "$limit": 0  # 0 returns count metadata
    }
    r_total = requests.get(BASE_URL, params=params_total, timeout=30)
    total_count = r_total.status_code
    
    # Query 2: Count with speed=-1 filter
    params_invalid = {
        "$select": "count(*)",
        "$where": f"time >= {date_start} AND time < {date_end} AND speed = -1",
        "$limit": 0
    }
    r_invalid = requests.get(BASE_URL, params=params_invalid, timeout=30)
    invalid_count = r_invalid.status_code
    
    # If $limit=0 doesn't give counts, we need to fetch records and count locally
    # Let's try with a small limit first to see the structure
    params_sample = {
        "$select": "time,speed",
        "$where": f"time >= {date_start} AND time < {date_end}",
        "$limit": 1  # just 1 record to test
    }
    r_sample = requests.get(BASE_URL, params=params_sample, timeout=30)
    
    print(f"  Total query status: {r_total.status_code}")
    print(f"  Invalid query status: {r_invalid.status_code}")
    print(f"  Sample query status: {r_sample.status_code}")
    print(f"  Sample records: {r_sample.json() if r_sample.status_code == 200 else 'N/A'}")
    
    # If $limit=0 doesn't work, fetch a small sample and count locally
    if r_sample.status_code == 200 and len(r_sample.json()) > 0:
        records = r_sample.json()
        # Count manually
        total_local = len(records)
        invalid_local = sum(1 for r in records if r.get("speed", "") == "-1")
        valid_local = total_local - invalid_local
        invalid_pct = invalid_local / total_local * 100 if total_local > 0 else 0
    else:
        # Fallback: use the status codes as indicators
        total_local = None
        invalid_local = None
        valid_local = None
        invalid_pct = None
    
    print(f"  Local count: total={total_local}, invalid={invalid_local}, valid={valid_local}, pct={invalid_pct:.1f}% if applicable")
    
    results.append({
        "date": date_str,
        "total_query_status": r_total.status_code,
        "invalid_query_status": r_invalid.status_code,
        "sample_status": r_sample.status_code if 'r_sample' in dir() else None,
        "total_count_status_code": total_count,
        "invalid_count_status": invalid_count,
    })

print("\n" + "=" * 60)
print("INVESTIGATION COMPLETE")
print("=" * 60)

# Save results
output_path = os.path.join("data", "processed", "daily_volume_summary.json")
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to: {output_path}")
PYEOF