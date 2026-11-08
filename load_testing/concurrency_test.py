import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


URL = "http://127.0.0.1:8000/api/v1/predict/batch"

RECORDS_PER_REQUEST = 1000
CONCURRENT_REQUESTS = 5


def create_records(count):
    records = []

    for i in range(count):
        records.append({
            "rd_spend": 10000 + (i % 490000),
            "admin_cost": 10000 + (i % 290000),
            "marketing_spend": 10000 + (i % 490000),
        })

    return records


PAYLOAD = {
    "records": create_records(RECORDS_PER_REQUEST)
}


def send_request(request_number):
    start_time = time.perf_counter()

    response = requests.post(
        URL,
        json=PAYLOAD,
        timeout=120,
    )

    elapsed_time = time.perf_counter() - start_time

    return {
        "request": request_number,
        "status_code": response.status_code,
        "elapsed_time": elapsed_time,
        "records_processed": (
            response.json().get("records_processed", 0)
            if response.status_code == 200
            else 0
        ),
    }


def main():
    print("ProfitIQ Concurrent API Test")
    print("============================")
    print(f"Concurrent requests : {CONCURRENT_REQUESTS}")
    print(f"Records/request     : {RECORDS_PER_REQUEST}")
    print(
        f"Total records       : "
        f"{CONCURRENT_REQUESTS * RECORDS_PER_REQUEST}"
    )

    start_time = time.perf_counter()

    results = []

    with ThreadPoolExecutor(
            max_workers=CONCURRENT_REQUESTS
    ) as executor:

        futures = [
            executor.submit(send_request, i + 1)
            for i in range(CONCURRENT_REQUESTS)
        ]

        for future in as_completed(futures):
            results.append(future.result())

    total_time = time.perf_counter() - start_time

    results.sort(key=lambda result: result["request"])

    print("\nIndividual Requests")
    print("-------------------")

    for result in results:
        print(
            f"Request {result['request']}: "
            f"{result['status_code']} | "
            f"{result['elapsed_time']:.4f}s | "
            f"{result['records_processed']} records"
        )

    successful_requests = sum(
        result["status_code"] == 200
        for result in results
    )

    total_records = sum(
        result["records_processed"]
        for result in results
    )

    print("\nSummary")
    print("-------")
    print(f"Successful requests : {successful_requests}/{CONCURRENT_REQUESTS}")
    print(f"Total time          : {total_time:.4f}s")
    print(f"Total records       : {total_records}")
    print(
        f"Overall throughput  : "
        f"{total_records / total_time:.2f} records/sec"
    )


if __name__ == "__main__":
    main()