import requests
from datetime import datetime
import json


def fetch_shows(page):
    response = requests.get("https://api.tvmaze.com/shows?page=" + str(page))
    if response.status_code == 404:
        return "Done"
    response = response.json()
    return response


def is_english(s):
    return s.isascii()


all_shows = {}
fetch = True
page = 0
while fetch:
    print(page)
    shows = fetch_shows(page=page)
    if shows == "Done":
        break
    for show in shows:
        if is_english(show["name"]):
            imdb = show["externals"]["imdb"]
            if imdb is None:
                print(show)
                continue
            if len(show["name"]) == 1:
                continue

            streaming = "N/A"
            network = ""
            if show["webChannel"] is None:
                pass
            else:
                streaming = show["webChannel"]["name"]
            if show["network"] is None:
                pass
            else:
                network = show["network"]["name"]

            all_shows[show["name"]] = {"streaming": streaming, "network": network, "mentions": 0, "score": 0,
                                       "consecutive": 0, "gain": 0, "total mentions": 0, "total top": 0, "last date": "",
                                       "total score": 0, "week added": 1}
    page += 1

date = datetime.today().strftime('%d-%m-%Y')

with open(f"{date}-allShows.json", "w") as file:
    file.write(json.dumps(all_shows))
