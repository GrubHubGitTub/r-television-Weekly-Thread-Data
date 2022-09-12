import requests
import json

"""Next fetch is only page 256, 257"""
def fetch_shows(page):
    response = requests.get("https://api.tvmaze.com/shows?page=" + str(page))
    response = response.json()
    print(page)
    return response


all_shows = {}
page = 1
while page < 257:
    shows = fetch_shows(page=page)
    for show in shows:
        all_shows[show["name"]] = {"mentions": 0}
    page += 1

with open("output.json", "r+") as file:
    file_data = json.load(file)
    file_data["shows"].append(all_shows)
    file.seek(0)
    json.dump(file_data, file, indent=4)