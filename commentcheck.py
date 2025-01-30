import pandas as pd
import json
import praw
from datetime import datetime, timedelta

# manual checks for common ways to say names on reddit
manual_checks = {
    "Love & Death": ['love and death'],
    "Class of '07": ["class of 07"],
    "Cunk on Earth": ["cunk"],
    "Lockwood & Co.": ["lockwood"],
    "Ginny & Georgia": ["ginny and georgia"],
    "Better Call Saul": ["bcs"],
    "That '90s Show": ["90s show", "90's show"],
    "The Last of Us": ["tlou"],
    "Star Wars: Andor": ["andor"],
    "DAHMER - Monster: The Jeffrey Dahmer Story": ["dahmer"],
    "She-Hulk: Attorney at Law": ["she-hulk", "she hulk"],
    "The Lord of the Rings: The Rings of Power": ["lord of the rings", "rings of power", "lotr"],
    "Cyberpunk: Edgerunners": ["cyberpunk"],
    "House of the Dragon": ["house of dragon", "hotd", "house of dragons"],
    "Mr. Robot": ["mr robot"],
    "Mr Inbetween": ["mr. inbetween"],
    "Guillermo del Toro's Cabinet of Curiosities": ["cabinet of curiosities"],
    "The Devil's Hour": ["the devils hour"],
    "Slow Horses": ["slow horse"],
    "SAS: Rogue Heroes": ["rogue heroes"],
    "Harry & Meghan": ["harry and meghan"],
    "The Witcher: Blood Origin": ["blood origin"],
    "Fleishman is in Trouble": ["fleishman"],
    "Love, Death & Robots": ["love death and robots", "love, death and robots", "love, death, and robots"],
    "Star Trek: Picard": ["picard"],
    "Pam & Tommy": ["pam and tommy"],
    "Winning Time: The Rise of the Lakers Dynasty": ["winning time"],
    "Arcane: League of Legends": ["arcane"],
    "Dune: Prophecy": ["dune", "dune prophecy", "dune : prophecy", "dune : prophesy", "dune prophesy"],
    "Monarch: Legacy of Monsters": ["monarch"],
    "The Lazarus Project": ["lazarus"],
    "The Traitors": ["traitors"],
    "Mr. & Mrs. Smith": ["mr and Mrs Smith", "mr & mrs Smith", "mr. and mrs. smith"],
    "Shogun": ["Shōgun"],
    "X-Men '97": ["x-men"],
    "A Man on the Inside": ["man on the inside", "the man on the inside"],
    "Star Wars: Skeleton Crew": ["skeleton crew"]
}

d = datetime.today()
date = d.strftime('%d-%m-%Y')

formatted = str(d.date())
tup = d.fromisoformat(formatted)
week_number = datetime.date(tup).isocalendar()[1]
print(f"it's week {week_number}")


reddit = praw.Reddit(
    client_id="efvqTOiFmiUSsHiNWOquig",
    client_secret="",
    user_agent="television fetch by u/Grubster11",
)

submission = reddit.submission("15ob8b1")
submission.comments.replace_more(limit=None)

with open(f"{date}-allShows.json", 'r') as json_file:
    weekly_data = json.load(json_file)

# with open("2022-allShows.json", 'r') as json_file:
#     weekly_data = json.load(json_file)

comment_number = 0
for comment in submission.comments.list():
    comment_number += 1
    print(comment_number)

    # skip my own comments
    if comment.author in ("Grubster11", "zrhodes3"):
        print("SKIP COMMENT")
        continue

    # comment check- make all words lowercase
    comment_lower = comment.body.lower()
    score = comment.score

    for show, details in weekly_data.items():

        # remove The for shows that start with it, can lead to some overcounts
        if len(show) > 10 and show[0:4] == "The ":
            show = show[4:]

        if show.lower() in comment_lower:
            details["mentions"] += 1
            details["score"] += score

        # some regex - it works, but undercounts due to lists, line ends
        ends = [" ","’", ",", ".", "!", "?",'"',"'","/",":", "&", ")", "(", "[","]","-","*"]
        match = False
        for end in ends:
            if f"{show.lower()}{end}" in comment_lower:
                details["regex-mentions"] += 1
                details["regex-score"] += score
                match = True
                break

        # for the case of a comment just being the name of a show, no ends.
        if not match:
            if show.lower() in comment_lower and len(show) == len(comment_lower):
                details["regex-mentions"] += 1
                details["regex-score"] += score

    for show, check_list in manual_checks.items():
        check_show = show
        if len(check_show) > 10 and check_show[0:4] == "The ":
            check_show = show[4:]
        for check in check_list:
            if check in comment_lower and show.lower() not in comment_lower:
                weekly_data[show]["mentions"] += 1
                weekly_data[show]["score"] += score
                break

# below is only used for the first week to add default values for comparison on next file
# for show, details in weekly_data.items():
#     weekly_data[show]["total mentions"] = weekly_data[show]["mentions"]
#     weekly_data[show]["total score"] = weekly_data[show]["score"]
#
#     if details["mentions"] >= 10:
#         weekly_data[show]["consecutive"] = 1
#         weekly_data[show]["gain"] = weekly_data[show]["mentions"]
#         weekly_data[show]["total top"] = 1

# check and compare with last week:


for i in range(1,12):
    last_week_date = (d - timedelta(days=i)).strftime('%d-%m-%Y')
    try:
        with open(f"{last_week_date}-allShows.json", 'r') as json_file:
            last_week = json.load(json_file)
            break
    except FileNotFoundError:
        pass
    # try:
    #     last_week_date = (d - timedelta(days=6)).strftime('%d-%m-%Y')
    #     with open(f"{last_week_date}-allShows.json", 'r') as json_file:
    #         last_week = json.load(json_file)
    # except FileNotFoundError:
    #     last_week_date = (d - timedelta(days=8)).strftime('%d-%m-%Y')
    #     with open(f"{last_week_date}-allShows.json", 'r') as json_file:
    #         last_week = json.load(json_file)

for show, details in weekly_data.items():

    match = False
    for key2, value2 in last_week.items():
        if show == key2:
            match = True
            weekly_data[show]["week added"] = value2["week added"]
            weekly_data[show]["total mentions"] = (value2["total mentions"] + weekly_data[show]["mentions"])
            weekly_data[show]["total score"] = (value2["total score"] + weekly_data[show]["score"])
            weekly_data[show]["total-regex-mentions"] = (value2["total-regex-mentions"] + weekly_data[show]["regex-mentions"])
            weekly_data[show]["total-regex-score"] = (value2["total-regex-score"] + weekly_data[show]["regex-score"])

            if details["mentions"] >= 10:
                # check last weeks weekly_data and add to consecutive number
                if value2["consecutive"] >= 1:
                    weekly_data[show]["consecutive"] = value2["consecutive"] + 1
                else:
                    weekly_data[show]["consecutive"] = 1
                    weekly_data[show]["last date"] = value2["last date"]
                weekly_data[show]["gain"] = weekly_data[show]["mentions"] - value2["mentions"]
                weekly_data[show]["total top"] += (value2["total top"] + 1)

            else:
                # save last date for next re appearance
                weekly_data[show]["consecutive"] = 0
                weekly_data[show]["total top"] = value2["total top"]
                if value2["consecutive"] >= 1:
                    weekly_data[show]["last date"] = last_week_date

    if not match:
        # add data for new show
        weekly_data[show]["total mentions"] = weekly_data[show]["mentions"]
        weekly_data[show]["total score"] = weekly_data[show]["score"]
        weekly_data[show]["week added"] = week_number
        weekly_data[show]["total-regex-mentions"] = weekly_data[show]["regex-mentions"]
        weekly_data[show]["total-regex-score"] = weekly_data[show]["regex-score"]

        if weekly_data[show]["mentions"] >= 10:
            weekly_data[show]["consecutive"] = 1
            weekly_data[show]["gain"] = weekly_data[show]["mentions"]
            weekly_data[show]["total top"] += 1


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
              "Together", "ToGetHer","Love", "Dark", "VICE", "Itch", "Anno", "Stone", "Honest", "Kings", "The Great Show",
              "The Game", "Television"]
this_week = this_week[~this_week.index.isin(skip_shows)]
this_week = this_week[this_week["mentions"] > 4]

this_week = this_week.sort_values(by=['mentions', 'score'], ascending=False)
this_week.to_csv(f"{date}-cleaned.csv")
