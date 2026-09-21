"""Test Chicago Traffic Tracker API using SODA2 endpoint with requests params for URL encoding.

Makes very small API requests to verify accessibility and schema.
Does NOT download the full dataset.
"""

import json
import time
import requests
import os

BASE_URL = "https://data.cityofchicago.org/resource/4g9f-3jbs.json"


def fetch_api(params, label=""):
    """Fetch data from the API using requests.params for automatic URL encoding."""
    print(f"=" * 60)
    print(f"API REQUEST: {label}")
    print("-" * 60)

    start_time = time.time()

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        http_status = response.status_code
        elapsed = time.time() - start_time

        print(f"HTTP STATUS CODE: {http_status}")
        print(f"REQUEST TIME: {elapsed:.2f} seconds")

        if http_status == 200:
            data = response.text
            records = json.loads(data)
            print(f"NUMBER OF RECORDS RETURNED: {len(records)}")

            if records:
                column_names = list(records[0].keys())
                print(f"COLUMN NAMES ({len(column_names)} columns):")
                for i, col in enumerate(column_names, 1):
                    print(f"  {i}. {col}")

                print(f"\nFIRST 5 RECORDS:")
                for i, record in enumerate(records[:5], 1):
                    print(f"  Record {i}: {json.dumps(record, indent=2)[:500]}")

                # Minimum and maximum TIME
                times = []
                speed_minus_1_count = 0
                missing_length_count = 0

                for record in records:
                    t = record.get("time", "")
                    if t:
                        times.append(t)
                    s = record.get("speed", "")
                    if s == "-1" or s == -1:
                        speed_minus_1_count += 1
                    l = record.get("length", "")
                    if l is None or l == "" or l == "null":
                        missing_length_count += 1

                if times:
                    print(f"\nMINIMUM TIME: {min(times)}")
                    print(f"MAXIMUM TIME: {max(times)}")
                else:
                    print("\nMINIMUM TIME: N/A")
                    print(f"MAXIMUM TIME: N/A")

                print(f"\nNUMBER OF SPEED = -1: {speed_minus_1_count}")
                print(f"NUMBER OF MISSING LENGTH: {missing_length_count}")
            else:
                print("NO RECORDS RETURNED (empty dataset)")
        else:
            print(f"HTTP ERROR: {http_status}")
            print("No records returned.")

        print("=" * 60 + "\n")

        return {
            "http_status": http_status,
            "request_time": elapsed,
            "records_returned": len(records) if http_status == 200 else 0,
            "succeeded": http_status == 200
        }
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"REQUEST FAILED: {type(e).__name__}: {e}")
        print(f"REQUEST TIME: {elapsed:.2f} seconds (failed)")
        print("=" * 60 + "\n")
        return {
            "http_status": None,
            "request_time": elapsed,
            "records_returned": 0,
            "succeeded": False
        }


def main():
    # Test 1: Time-filtered query with $select and $limit=100
    params1 = {
        "$select": "time,segment_id,speed,length,hour,day_of_week,month",
        "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-12T00:00:00'",
        "$limit": 100
    }
    result1 = fetch_api(params1, "TEST 1: Time-filtered query June 11, 2024 LIMIT 100")

    # Test 2: Same one-day period with $limit=5000 and additional columns
    params2 = {
        "$select": "time,segment_id,speed,length,bus_count,message_count,hour,day_of_week,month",
        "$where": "time >= '2024-06-11T00:00:00' AND time < '2024-06-12T00:00:00'",
        "$limit": 5000
    }
    result2 = fetch_api(params2, "TEST 2: One-day period LIMIT 5000")

    print("\n--- INVESTIGATION COMPLETE ---")
    print("No ML models trained.")
    print("No synthetic data created.")
    print("No 101M+ row dataset downloaded.")


if __name__ == "__main__":
    main()