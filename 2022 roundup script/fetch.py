import pandas as pd
import json
import praw

threads = []
with open("threads.txt", "r") as file:
    Lines = file.readlines()
    for line in Lines:
        thread = line[45:51]
        threads.append(thread)
reddit = praw.Reddit(
    client_id="efvqTOiFmiUSsHiNWOquig",
    client_secret="",
    user_agent="television fetch by u/Grubster11",
)
week = 6
for thread in threads[week-1:]:
    print("getting")
    submission = reddit.submission(thread)
    print("thread")
    submission.comments.replace_more(limit=None)
    print("now")

    with open("2022-allShows.json", 'r') as json_file:
        weekly_data = json.load(json_file)

    comment_number = 0
    for comment in submission.comments.list():
        comment_number += 1
        print(comment_number)

        # skip my own comments
        if comment.author in ("Grubster11", "zrhodes3"):
            print("SKIP COMMENT")
            continue

        # comment check- make all words lowercase
        lower = comment.body.comment_lower()
        score = comment.score
        for key, value in weekly_data.items():
            # if len(show) <= 3:
            #     continue
            # if show in skip_shows:
            #     continue
            if key.comment_lower() in lower:
                value["mentions"] += 1
                value["score"] += score

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

        if "mandalorian" in lower and "The Mandalorian".lower() not in lower:
            weekly_data["The Mandalorian"]["mentions"] += 1
            weekly_data["The Mandalorian"]["score"] += score

        if ("love death and robots" in lower or "love, death and robots" in lower or "love, death, and robots" in lower) and \
            "Love, Death & Robots".lower() not in lower:
            weekly_data["Love, Death & Robots"]["mentions"] += 1
            weekly_data["Love, Death & Robots"]["score"] += score

        if "picard" in lower and "Star Trek: Picard".lower() not in lower:
            weekly_data["Star Trek: Picard"]["mentions"] += 1
            weekly_data["Star Trek: Picard"]["score"] += score

        if "pam and tommy" in lower and "Pam & Tommy".lower() not in lower:
            weekly_data["Pam & Tommy"]["mentions"] += 1
            weekly_data["Pam & Tommy"]["score"] += score

        if "winning time" in lower and "Winning Time: The Rise of the Lakers Dynasty".lower() not in lower:
            weekly_data["Winning Time: The Rise of the Lakers Dynasty"]["mentions"] += 1
            weekly_data["Winning Time: The Rise of the Lakers Dynasty"]["score"] += score

    with open(f"{week}-allShows.json", "w") as file:
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
    this_week = this_week[this_week["mentions"] > 0]

    this_week = this_week.sort_values(by=['mentions', 'score'], ascending=False)
    this_week.to_csv(f"{week}-cleaned.csv")

    print(f"done week {week}")
    week += 1
