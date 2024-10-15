import json
import os
import requests
import time

HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "X-Api-Key": "mixamo2",
    "X-Requested-With": "XMLHttpRequest",
}

session = requests.Session()

def make_request(method, url, **kwargs):
    for _ in range(10):  # Retry 10 times
        try:
            response = session.request(method, url, timeout=10, **kwargs)                
            return response
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            time.sleep(1)
            continue
    raise Exception(f"Failed to complete request to {url} after 10 retries.")

def get_animations_data():
    params = {
      "limit": 96,
      "page": 0,
      "type": "Motion",
      #"query": query,
    }
    response = make_request("GET", "https://www.mixamo.com/api/v1/products", headers=HEADERS, params=params)
    data = response.json()
    num_pages = data["pagination"]["num_pages"]
    animations = []

    print(f"numpages={num_pages}")

    # for some reason, it seems not all animations are returned in a single pass.
    # Therefore we run the query multiple times and then de-duplicate to ensure all animations are included.
    runs = 20
    for run in range(runs):
        print(f'run={run+1}/{runs}')
        for page_num in range(num_pages+1):
            print(f"  page={page_num}")
            params["page"] = page_num
            response = make_request("GET", "https://www.mixamo.com/api/v1/products", headers=HEADERS, params=params)
            data = response.json()
            animations.extend(data["results"])
        print(f"  total={len(animations)}")

    anim_data = {animation["id"]: animation["description"] for animation in animations}
    return anim_data

ans = get_animations_data()
print(f"found {len(ans)} unique animations")

with open("ans.json", 'w') as json_file:
    json.dump(ans, json_file, indent=4)  # `indent=4` for pretty printing