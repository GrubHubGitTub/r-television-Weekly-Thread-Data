import requests
import json

"""Next fetch is only page 256, 257"""
def fetch_shows(page):
    response = requests.get("https://api.tvmaze.com/shows?page=" + str(page))
    if response.status_code == 404:
        return "Done"
    response = response.json()
    return response


all_shows = {}
fetch = True
page = 0
while fetch:
    print(page)
    shows = fetch_shows(page=page)
    if shows == "Done":
        break
    for show in shows:
        imdb = show["externals"]["imdb"]
        if imdb is None:
            print(show)
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

        all_shows[show["name"]] = {"network":network, "streaming": streaming, "imdb":imdb, "mentions": 0, "score":0}
    page += 1

with open("AllShows.json", "r+") as file:
    json.dump(all_shows, file, indent=4)