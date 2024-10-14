import json
import os
import requests
import time
from PySide2 import QtCore, QtWebEngineWidgets, QtWidgets

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

def get_queried_animations_data():
    page_num = 0
    params = {
      "limit": 96,
      "page": page_num,
      "type": "Motion",
      #"query": query,
    }
    response = make_request("GET", "https://www.mixamo.com/api/v1/products", headers=HEADERS, params=params)
    data = response.json()
    num_pages = data["pagination"]["num_pages"]
    animations = []

    #num_pages = 3
    print(f"numpages={num_pages}")

    for _ in range(20):
        page_num = 0
        while page_num <= num_pages:
            print(f"page={page_num}")
            params["page"] = page_num
            response = make_request("GET", "https://www.mixamo.com/api/v1/products", headers=HEADERS, params=params)
            data = response.json()
            #print(len(data["results"])) # 96
            #print(data["results"])
            animations.extend(data["results"])
            page_num += 1
        print(f"total={len(animations)}")

    #anim_data = [f'{animation["motion_id"]}{animation["description"]}' for animation in animations]
    anim_data = {animation["id"]: animation["description"] for animation in animations}
    return anim_data

ans = get_queried_animations_data()
print(f"found {len(ans)}")

with open("ans.json", 'w') as json_file:
    json.dump(ans, json_file, indent=4)  # `indent=4` for pretty printing