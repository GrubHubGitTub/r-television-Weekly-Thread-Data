import pandas as pd
import json
import praw
from datetime import datetime, timedelta

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

submission = reddit.submission("138ra4k")
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
    if comment.author == "Grubster11":
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

    # manual checks for common ways to say names on reddit
    if "love and death" in comment_lower and "Love & Death".lower() not in comment_lower:
        weekly_data["Love & Death"]["mentions"] += 1
        weekly_data["Love & Death"]["score"] += score

    if "class of 07" in comment_lower and "Class of '07".lower() not in comment_lower:
        weekly_data["Class of '07"]["mentions"] += 1
        weekly_data["Class of '07"]["score"] += score

    if "cunk" in comment_lower and "Cunk on Earth".lower() not in comment_lower:
        weekly_data["Cunk on Earth"]["mentions"] += 1
        weekly_data["Cunk on Earth"]["score"] += score

    if "lockwood" in comment_lower and "Lockwood & Co.".lower() not in comment_lower:
        weekly_data["Lockwood & Co."]["mentions"] += 1
        weekly_data["Lockwood & Co."]["score"] += score

    if "ginny and georgia" in comment_lower and "Ginny & Georgia".lower() not in comment_lower:
        weekly_data["Ginny & Georgia"]["mentions"] += 1
        weekly_data["Ginny & Georgia"]["score"] += score

    if "bcs" in comment_lower and "Better Call Saul".lower() not in comment_lower:
        weekly_data["Better Call Saul"]["mentions"] += 1
        weekly_data["Better Call Saul"]["score"] += score

    if ("90s show" in comment_lower or "90's show" in comment_lower) and \
            "That '90s Show".lower() not in comment_lower:
        weekly_data["That '90s Show"]["mentions"] += 1
        weekly_data["That '90s Show"]["score"] += score

    if "tlou" in comment_lower and "last of us" not in comment_lower:
        weekly_data["The Last of Us"]["mentions"] += 1
        weekly_data["The Last of Us"]["score"] += score

    if "andor" in comment_lower and "star wars: andor" not in comment_lower:
        weekly_data["Star Wars: Andor"]["mentions"] += 1
        weekly_data["Star Wars: Andor"]["score"] += score

    if "dahmer" in comment_lower and "Monster: The Jeffrey Dahmer Story".lower() not in comment_lower:
        weekly_data["DAHMER - Monster: The Jeffrey Dahmer Story"]["mentions"] += 1
        weekly_data["DAHMER - Monster: The Jeffrey Dahmer Story"]["score"] += score

    if ("she hulk" in comment_lower or "she-hulk" in comment_lower) and "She-Hulk: Attorney at Law".lower() not in comment_lower:
        weekly_data["She-Hulk: Attorney at Law"]["mentions"] += 1
        weekly_data["She-Hulk: Attorney at Law"]["score"] += score

    if ("lord of the rings" in comment_lower or "rings of power" in comment_lower or "lotr" in comment_lower) \
            and "The Lord of the Rings: The Rings of Power".lower() not in comment_lower:
        weekly_data["The Lord of the Rings: The Rings of Power"]["mentions"] += 1
        weekly_data["The Lord of the Rings: The Rings of Power"]["score"] += score

    if "cyberpunk" in comment_lower and "Cyberpunk: Edgerunners".lower() not in comment_lower:
        weekly_data["Cyberpunk: Edgerunners"]["mentions"] += 1
        weekly_data["Cyberpunk: Edgerunners"]["score"] += score

    if ("house of dragon" in comment_lower or "hotd" in comment_lower or "house of dragons" in comment_lower) \
            and "House of the Dragon".lower() not in comment_lower:
        weekly_data["House of the Dragon"]["mentions"] += 1
        weekly_data["House of the Dragon"]["score"] += score

    if "mr robot" in comment_lower and "Mr. Robot".lower() not in comment_lower:
        weekly_data["Mr. Robot"]["mentions"] += 1
        weekly_data["Mr. Robot"]["score"] += score

    if "mr. inbetween" in comment_lower and "Mr Inbetween".lower() not in comment_lower:
        weekly_data["Mr Inbetween"]["mentions"] += 1
        weekly_data["Mr Inbetween"]["score"] += score

    if "cabinet of curiosities" in comment_lower and "Guillermo del Toro's Cabinet of Curiosities".lower() not in comment_lower:
        weekly_data["Guillermo del Toro's Cabinet of Curiosities"]["mentions"] += 1
        weekly_data["Guillermo del Toro's Cabinet of Curiosities"]["score"] += score

    if "the devils hour" in comment_lower and "The Devil's Hour".lower() not in comment_lower:
        weekly_data["The Devil's Hour"]["mentions"] += 1
        weekly_data["The Devil's Hour"]["score"] += score

    if "slow horse" in comment_lower and "Slow Horses".lower() not in comment_lower:
        weekly_data["Slow Horses"]["mentions"] += 1
        weekly_data["Slow Horses"]["score"] += score

    if "rogue heroes" in comment_lower and "SAS: Rogue Heroes".lower() not in comment_lower:
        weekly_data["SAS: Rogue Heroes"]["mentions"] += 1
        weekly_data["SAS: Rogue Heroes"]["score"] += score

    if "harry and meghan" in comment_lower and "Harry & Meghan".lower() not in comment_lower:
        weekly_data["Harry & Meghan"]["mentions"] += 1
        weekly_data["Harry & Meghan"]["score"] += score

    if "blood origin" in comment_lower and "The Witcher: Blood Origin".lower() not in comment_lower:
        weekly_data["The Witcher: Blood Origin"]["mentions"] += 1
        weekly_data["The Witcher: Blood Origin"]["score"] += score

    if "fleishman" in comment_lower and "Fleishman is in Trouble".lower() not in comment_lower:
        weekly_data["Fleishman is in Trouble"]["mentions"] += 1
        weekly_data["Fleishman is in Trouble"]["score"] += score

    if ("love death and robots" in comment_lower or "love, death and robots" in comment_lower or "love, death, and robots" in comment_lower) and \
            "Love, Death & Robots".lower() not in comment_lower:
        weekly_data["Love, Death & Robots"]["mentions"] += 1
        weekly_data["Love, Death & Robots"]["score"] += score

    if "picard" in comment_lower and "Star Trek: Picard".lower() not in comment_lower:
        weekly_data["Star Trek: Picard"]["mentions"] += 1
        weekly_data["Star Trek: Picard"]["score"] += score

    if "pam and tommy" in comment_lower and "Pam & Tommy".lower() not in comment_lower:
        weekly_data["Pam & Tommy"]["mentions"] += 1
        weekly_data["Pam & Tommy"]["score"] += score

    if "winning time" in comment_lower and "Winning Time: The Rise of the Lakers Dynasty".lower() not in comment_lower:
        weekly_data["Winning Time: The Rise of the Lakers Dynasty"]["mentions"] += 1
        weekly_data["Winning Time: The Rise of the Lakers Dynasty"]["score"] += score

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
