"""Investigate data volume and temporal coverage of Chicago Traffic Tracker API."""

import requests
import json
import time

BASE_URL = 'https://data.cityofchicago.org/resource/4g9f-3jbs.json'


def api_query(params, label=""):
    """Make API query and return results."""
    print("=" * 60)
    print(f"API QUERY: {label}")
    start = time.time()
    try:
        r = requests.get(BASE_URL, params=params, timeout=60)
        elapsed = time.time() - start
        print(f"HTTP STATUS: {r.status_code}")
        print(f"REQUEST TIME: {elapsed:.2f}s")
        print(f"RETURNED ROWS: {len(r.json()) if r.status_code == 200 else 0}")
        print("=" * 60 + "\n")
        return {"status": r.status_code, "time": elapsed, "data": r.json() if r.status_code == 200 else None}
    except Exception as e:
        elapsed = time.time() - start
        print(f"ERROR: {type(e).__name__}: {str(e)[:100]}")
        print(f"REQUEST TIME: {elapsed:.2f}s")
        print("=" * 60 + "\n")
        return {"status": None, "time": elapsed, "data": None}


# TEST 1: Try date extraction
print("TEST 1: Date extraction attempt")
params1 = {
    "$select": "time",
    "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-18T00:00:00'",
    "$limit": 0  # 0 means no data rows, just metadata/aggregation info
}
result1 = api_query(params1, "Count by date range")

# TEST 2: Count by hour within one day
print("\nTEST 2: Count by hour (one day)")
params2 = {
    "$select": "hour,count(*) as records",
    "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-12T00:00:00'",
    "$group_by": "hour",
    "$order_by": "hour",
    "$limit": 0
}
result2 = api_query(params2, "Count by hour")

# TEST 3: Speed quality by day
print("\nTEST 3: Speed quality by day")
params3 = {
    "$select": "time",
    "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-18T00:00:00'",
    "$limit": 0
}
result3 = api_query(params3, "Speed quality by day - fetch sample")

# Print first few records to see date format
if result3["data"]:
    dates = set()
    for rec in result3["data"][:20]:
        t = rec.get("time", "")
        if t and len(t) >= 4:
            dates.add(t[:4])
    print("Years observed in sample:", sorted(dates))

# TEST 4: Segment coverage
print("\nTEST 4: Segment coverage (one day)")
params4 = {
    "$select": "segment_id,count(*) as records",
    "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-12T00:00:00'",
    "$group_by": "segment_id",
    "$order_by": "records DESC",
    "$limit": 0
}
result4 = api_query(params4, "Segment coverage")

# If group_by not supported, try alternative: fetch sample and compute locally
if result4["status"] != 200 or result4["data"] is None:
    print("\n--- ALTERNATIVE: Fetch sample and compute segment counts locally ---")
    params4f = {
        "$select": "segment_id",
        "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-12T00:00:00'",
        "$limit": 5000
    }
    result4f = api_query(params4f, "Segment sample (5000)")
    if result4f["data"] and len(result4f["data"]) > 0:
        seg_counts = {}
        for rec in result4f["data"]:
            sid = rec.get("segment_id", "")
            if sid:
                seg_counts[sid] = seg_counts.get(sid, 0) + 1
        # Top 20
        top20 = sorted(seg_counts.items(), key=lambda x: x[1], reverse=True)[:20]
        print("TOP 20 SEGMENTS by observation count:")
        for sid, cnt in top20:
            print(f"  segment_id={sid}: {cnt} observations")
        print(f"Total unique segments in sample: {len(seg_counts)}")

print("\n" + "=" * 60)
print("INVESTIGATION COMPLETE")
PYEOF