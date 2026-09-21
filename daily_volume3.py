"""Daily volume investigation - proper version."""

import requests
import json
import os
from datetime import datetime, timedelta

BASE_URL = 'https://data.cityofchicago.org/resource/4g9f-3jbs.json'

dates = [
    "2024-06-11",
    "2024-06-12",
    "2024-06-13",
    "2024-06-14",
    "2024-06-15",
    "2024-06-16",
    "2024-06-17"
]

results = []

for date_str in dates:
    print(f"\nProcessing {date_str}...")
    
    # Calculate date range
    d = datetime.strptime(date_str, "%Y-%m-%d")
    next_d = (d + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    date_start = f"'{date_str}T00:00:00'"
    date_end = f"'{next_d}'"
    
    # Fetch sample of 200 records for this date range
    params = {
        "$select": "time,speed",
        "$where": f"time >= {date_start} AND time < {date_end}",
        "$limit": 200
    }
    r = requests.get(BASE_URL, params=params, timeout=30)
    
    if r.status_code == 200 and len(r.json()) > 0:
        records = r.json()
        total_local = len(records)
        invalid_local = sum(1 for r in records if r.get("speed", "") == "-1")
        valid_local = total_local - invalid_local
        invalid_pct = invalid_local / total_local * 100 if total_local > 0 else 0
    else:
        total_local = None
        invalid_local = None
        valid_local = None
        invalid_pct = None
    
    results.append({
        "date": date_str,
        "total_query_status": r.status_code,
        "total_records_local": total_local,
        "invalid_local": invalid_local,
        "valid_local": valid_local,
        "invalid_pct": invalid_pct
    })
    
    print(f"{date_str}: total_local={total_local}, invalid={invalid_local}, pct={invalid_pct:.1f}% if applicable")

print("\n" + "=" * 60)
print("RESULTS SAVED")

# Save
output_path = os.path.join("data", "processed", "daily_volume_summary.json")
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

# Calculate summary stats
valid_results = [r for r in results if r["total_records_local"] is not None]
if valid_results:
    counts = [r["total_records_local"] for r in valid_results]
    pcts = [r["invalid_pct"] for r in valid_results if r["invalid_pct"] is not None]
    
    print(f"\nAverage records/day: {sum(counts)/len(counts):.1f}")
    print(f"Min daily records: {min(counts)}")
    print(f"Max daily records: {max(counts)}")
    if pcts:
        print(f"Average invalid-speed percentage: {sum(pcts)/len(pcts):.1f}%")