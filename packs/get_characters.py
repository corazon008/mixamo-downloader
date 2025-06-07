import json
import os
import requests
import time
import re

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

def get_character_data():
    params = {
      "limit": 96,
      "page": 0,
      "type": "Character",
      #"query": query,
    }
    response = make_request("GET", "https://www.mixamo.com/api/v1/products", headers=HEADERS, params=params)
    data = response.json()
    num_pages = data["pagination"]["num_pages"]
    characters = []

    print(f"numpages={num_pages}")

    # for some reason, it seems not all items are returned in a single pass.
    # Therefore we run the query multiple times and then de-duplicate to ensure all items are included.
    runs = 1
    for run in range(runs):
        print(f'run={run+1}/{runs}')
        for page_num in range(num_pages+1):
            print(f"  page={page_num}")
            params["page"] = page_num
            response = make_request("GET", "https://www.mixamo.com/api/v1/products", headers=HEADERS, params=params)
            data = response.json()
            characters.extend(data["results"])
        print(f"  total={len(characters)}")

    char_data = {character["id"]: character for character in characters}
    return char_data

def make_table(characters):
    with open('characters_table.md', 'w') as file:
        file.write(f"| ID | Name | Media |\n")
        file.write(f"|----|------|-------|\n")
        for id, character in characters.items():
            assert character['type'] == 'Character'
            assert character['description'] == ''
            assert character['category'] == ''
            assert character['character_type'] == 'human'
            #media_id = re.search(r'/characters/([\d-]+)/', character['thumbnail']).group(1)
            id   = character['id']
            assert character['thumbnail'] == f'https://www.mixamo.com/api/v1/characters/{id}/assets/thumbnails/static.png'
            assert character['thumbnail_animated'] == character['thumbnail']
            assert character['motion_id'] == None
            assert character['motions'] == None
            assert character['source'] == 'system'
            #file.write(f"| {character['id']} | {character['name']} | ![PNG]({character['thumbnail']}) |\n")
            imgsrc = character['thumbnail']
            file.write(f"| {character['id']} | {character['name']} | <img src=\"{imgsrc}\" height=\"60\" > [PNG]({imgsrc}) |\n")


characters = get_character_data()
print(f"found {len(characters)} unique characters")

#anim_ans = {anim['id']: anim['description'] for id, anim in animations.items()}
with open("mixamo_chars.json", 'w') as json_file:
    json.dump(characters, json_file, indent=4)  # `indent=4` for pretty printing

make_table(characters)