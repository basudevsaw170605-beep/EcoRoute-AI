"""Test different API query formats."""

import requests

BASE_URL = 'https://data.cityofchicago.org/resource/4g9f-3jbs.json'

# Test 1: Simple limit
r = requests.get(BASE_URL, params={"$limit": 5}, timeout=30)
print(f"Test 1 - $limit=5: status={r.status_code}, records={len(r.json()) if r.status_code == 200 else 'N/A'}")

# Test 2: With $where
r2 = requests.get(BASE_URL, params={"$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-12T00:00:00'"}, timeout=30)
print(f"Test 2 - $where: status={r2.status_code}, records={len(r2.json()) if r2.status_code == 200 else 'N/A'}")

# Test 3: With $select and $where
r3 = requests.get(BASE_URL, params={"$select": "count(*)", "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-12T00:00:00'"}, timeout=30)
print(f"Test 3 - $select count + $where: status={r3.status_code}")

# Test 4: Just count with $select
r3b = requests.get(BASE_URL, params={"$select": "count(*)"}, timeout=30)
print(f"Test 3b - $select count only: status={r3b.status_code}")