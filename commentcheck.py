import pandas as pd
import json
import praw
from datetime import datetime, timedelta

d = datetime.today()
date = d.strftime('%d-%m-%Y')
last_week_date = (d - timedelta(days=7)).strftime('%d-%m-%Y')

formatted = str(d.date())
tup = d.fromisoformat(formatted)
week_number = datetime.date(tup).isocalendar()[1]

reddit = praw.Reddit(
    client_id="efvqTOiFmiUSsHiNWOquig",
    client_secret="",
    user_agent="television fetch by u/Grubster11",
)

submission = reddit.submission("ztkf4x")
submission.comments.replace_more(limit=None)

with open(f"{date}-allShows.json", 'r') as json_file:
    weekly_data = json.load(json_file)

comment_number = 0
for comment in submission.comments.list():
    comment_number += 1
    print(comment_number)

    # skip my own comments
    if comment.author == "Grubster11":
        print("SKIP COMMENT")
        continue

    # comment check- make all words lowercase
    lower = comment.body.lower()
    score = comment.score
    for key, value in weekly_data.items():
        # if len(key) <= 3:
        #     continue
        # if key in skip_shows:
        #     continue
        if key.lower() in lower:
            value["mentions"] += 1
            value["score"] += score
            print(key)

    # manual checks for common ways to say names on reddit
    if "andor" in lower and "star wars: andor" not in lower:
        weekly_data["Star Wars: Andor"]["mentions"] += 1
        weekly_data["Star Wars: Andor"]["score"] += score

    if "dahmer" in lower and "Monster: The Jeffrey Dahmer Story".lower() not in lower:
        weekly_data["Monster: The Jeffrey Dahmer Story"]["mentions"] += 1
        weekly_data["Monster: The Jeffrey Dahmer Story"]["score"] += score

    if ("she hulk" in lower or "she-hulk" in lower) and "She-Hulk: Attorney at Law".lower() not in lower:
        weekly_data["She-Hulk: Attorney at Law"]["mentions"] += 1
        weekly_data["She-Hulk: Attorney at Law"]["score"] += score

    if ("lord of the rings" in lower or "rings of power" in lower or "lotr" in lower) \
            and "The Lord of the Rings: The Rings of Power".lower() not in lower:
        weekly_data["The Lord of the Rings: The Rings of Power"]["mentions"] += 1
        weekly_data["The Lord of the Rings: The Rings of Power"]["score"] += score

    if "sandman" in lower and "The Sandman".lower() not in lower:
        weekly_data["The Sandman"]["mentions"] += 1
        weekly_data["The Sandman"]["score"] += score

    if "cyberpunk" in lower and "Cyberpunk: Edgerunners".lower() not in lower:
        weekly_data["Cyberpunk: Edgerunners"]["mentions"] += 1
        weekly_data["Cyberpunk: Edgerunners"]["score"] += score

    if ("house of dragon" in lower or "hotd" in lower or "house of dragons" in lower) \
            and "House of the Dragon".lower() not in lower:
        weekly_data["House of the Dragon"]["mentions"] += 1
        weekly_data["House of the Dragon"]["score"] += score

    if ("mr robot" in lower) and "Mr. Robot".lower() not in lower:
        weekly_data["Mr. Robot"]["mentions"] += 1
        weekly_data["Mr. Robot"]["score"] += score

    if ("mr. inbetween" in lower) and "Mr Inbetween".lower() not in lower:
        weekly_data["Mr Inbetween"]["mentions"] += 1
        weekly_data["Mr Inbetween"]["score"] += score

    if ("cabinet of curiosities" in lower) and "Guillermo del Toro's Cabinet of Curiosities".lower() not in lower:
        weekly_data["Guillermo del Toro's Cabinet of Curiosities"]["mentions"] += 1
        weekly_data["Guillermo del Toro's Cabinet of Curiosities"]["score"] += score

    if ("the devils hour" in lower) and "The Devil's Hour".lower() not in lower:
        weekly_data["The Devil's Hour"]["mentions"] += 1
        weekly_data["The Devil's Hour"]["score"] += score

    if "white lotus" in lower and "The White Lotus".lower() not in lower:
        weekly_data["The White Lotus"]["mentions"] += 1
        weekly_data["The White Lotus"]["score"] += score

    if "slow horse" in lower and "Slow Horses".lower() not in lower:
        weekly_data["Slow Horses"]["mentions"] += 1
        weekly_data["Slow Horses"]["score"] += score

    if "rogue heroes" in lower and "SAS: Rogue Heroes".lower() not in lower:
        weekly_data["SAS: Rogue Heroes"]["mentions"] += 1
        weekly_data["SAS: Rogue Heroes"]["score"] += score

    if "harry and meghan" in lower and "Harry & Meghan".lower() not in lower:
        weekly_data["Harry & Meghan"]["mentions"] += 1
        weekly_data["Harry & Meghan"]["score"] += score

    if "blood origin" in lower and "The Witcher: Blood Origin".lower() not in lower:
        weekly_data["The Witcher: Blood Origin"]["mentions"] += 1
        weekly_data["The Witcher: Blood Origin"]["score"] += score

    if "fleishman" in lower and "Fleishman is in Trouble".lower() not in lower:
        weekly_data["Fleishman is in Trouble"]["mentions"] += 1
        weekly_data["Fleishman is in Trouble"]["score"] += score

# below is only used for the first week to add default values for comparison on next file
for key, value in weekly_data.items():
    weekly_data[key]["total mentions"] = weekly_data[key]["mentions"]
    weekly_data[key]["total score"] = weekly_data[key]["score"]

    if value["mentions"] >= 10:
        weekly_data[key]["consecutive"] = 1
        weekly_data[key]["gain"] = weekly_data[key]["mentions"]
        weekly_data[key]["total top"] = 1

# # check and compare with last week:
# try:
#     with open(f"{last_week_date}-allShows.json", 'r') as json_file:
#         last_week = json.load(json_file)
#
# except FileNotFoundError:
#     try:
#         last_week_date = (d - timedelta(days=6)).strftime('%d-%m-%Y')
#         with open(f"{last_week_date}-allShows.json", 'r') as json_file:
#             last_week = json.load(json_file)
#     except FileNotFoundError:
#         last_week_date = (d - timedelta(days=8)).strftime('%d-%m-%Y')
#         with open(f"{last_week_date}-allShows.json", 'r') as json_file:
#             last_week = json.load(json_file)
#
# for key, value in weekly_data.items():
#
#     match = False
#     for key2, value2 in last_week.items():
#         if key == key2:
#             match = True
#             weekly_data[key]["week added"] = value2["week added"]
#             weekly_data[key]["total mentions"] = (value2["total mentions"] + weekly_data[key]["mentions"])
#             weekly_data[key]["total score"] = (value2["total score"] + weekly_data[key]["score"])

#             if value["mentions"] >= 10:
#                 # check last weeks weekly_data and add to consecutive number
#                 if value2["consecutive"] >= 1:
#                     weekly_data[key]["consecutive"] = value2["consecutive"] + 1
#                 else:
#                     weekly_data[key]["consecutive"] = 1
#                     weekly_data[key]["last date"] = value2["last date"]
#                 weekly_data[key]["gain"] = weekly_data[key]["mentions"] - value2["mentions"]
#                 weekly_data[key]["total top"] += (value2["total top"] + 1)
#
#             else:
#                 # save last date for next re appearance
#                 weekly_data[key]["consecutive"] = 0
#                 if value2["consecutive"] >= 1:
#                     weekly_data[key]["last date"] = last_week_date
#
#     if not match:
#         # add data for new show
#         weekly_data[key]["total mentions"] = weekly_data[key]["mentions"]
#         weekly_data[key]["total score"] = weekly_data[key]["score"]
#         weekly_data[key]["week added"] = week_number
#
#         if weekly_data[key]["mentions"] >= 10:
#             weekly_data[key]["consecutive"] = 1
#             weekly_data[key]["gain"] = weekly_data[key]["mentions"]
#             weekly_data[key]["total top"] += 1


with open(f"{date}-allShows.json", "w") as file:
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
this_week = this_week[this_week["mentions"] > 4]

this_week = this_week.sort_values(by=['mentions', 'score'], ascending=False)
this_week.to_csv(f"{date}-cleaned.csv")
