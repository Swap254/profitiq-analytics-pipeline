import time

import requests


URL = "http://127.0.0.1:8000/api/v1/predict/batch"

TEST_SIZES = [10, 100, 1000, 5000, 10000]


def create_records(count):
    records = []

    for i in range(count):
        records.append({
            "rd_spend": 10000 + (i % 490000),
            "admin_cost": 10000 + (i % 290000),
            "marketing_spend": 10000 + (i % 490000),
        })

    return records


def run_test(record_count):
    payload = {
        "records": create_records(record_count)
    }

    start_time = time.perf_counter()

    response = requests.post(
        URL,
        json=payload,
        timeout=120,
    )

    elapsed_time = time.perf_counter() - start_time

    print(f"\nRecords       : {record_count}")
    print(f"Status code   : {response.status_code}")
    print(f"Time          : {elapsed_time:.4f} seconds")

    if response.status_code == 200:
        result = response.json()

        print(f"Processed     : {result['records_processed']}")
        print(
            f"Throughput    : "
            f"{result['records_processed'] / elapsed_time:.2f} records/sec"
        )
    else:
        print(f"Response      : {response.text}")


def main():
    print("ProfitIQ Batch API Load Test")
    print("============================")

    for size in TEST_SIZES:
        run_test(size)


if __name__ == "__main__":
    main()