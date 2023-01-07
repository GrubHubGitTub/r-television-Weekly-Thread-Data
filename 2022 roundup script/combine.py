import pandas as pd
import json

with open("2022-allShows.json", "r") as json_file:
    weekly_data = json.load(json_file)

for key, value in weekly_data.items():
    weekly_data[key]["week added"] = 0
    weekly_data[key]["largest week"] = 0
    weekly_data[key]["largest week amt"] = 0

for n in range(1,51):
    with open(f"{n}-allShows.json") as file:
        week = json.load(file)
    for key, value in weekly_data.items():
        if weekly_data[key]["week added"] == 0 and week[key]["mentions"] > 0:
            weekly_data[key]["week added"] = n

        if week[key]["mentions"] > weekly_data[key]["largest week amt"]:
            weekly_data[key]["largest week"] = n
            weekly_data[key]["largest week amt"] = week[key]["mentions"]

        weekly_data[key]["mentions"] += week[key]["mentions"]
        weekly_data[key]["score"] += week[key]["score"]

with open("2022-allShows-totals.json", "w") as file:
    file.write(json.dumps(weekly_data))

# create DF and CSV
this_week = pd.DataFrame(weekly_data)
this_week = this_week.T
this_week.index.name = 'name'
this_week = this_week[~(this_week.index.str.len() < 4)]
skip_shows = ["Ally", "Really", "Star", "King", "From", "Time", "Arte", "The First", "The Show", "Bette", "Last",
              "Next", "neXt", "Don't", "Them", "Hile", "Vera", "Drama", "The Story", "Stat", "Before",
              "Another", "Roba", "Back", "Hard", "Haven", "Made", "High", "Look", "Episodes", "Hank", "Times",
              "Land", "Ellen", "Action", "Rise", "Found", "Between", "Mila", "Help", "Sever", "Thanks", "The End",
              "Looking", "Live", "Life", "LIFE", "Origin", "Else", "Girls", "GIRLS", "Absolutely", "Special", "Lace",
              "Together", "ToGetHer"]
this_week = this_week[~this_week.index.isin(skip_shows)]

this_week = this_week[["streaming","network", "mentions", "score", "week added", "largest week", "largest week amt"]]
this_week = this_week.sort_values(by=['mentions', 'score'], ascending=False)
this_week.to_csv("2022-cleaned.csv")