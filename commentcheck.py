import pandas as pd
import json
import praw
from datetime import datetime

reddit = praw.Reddit(
    client_id= "efvqTOiFmiUSsHiNWOquig",
    client_secret= "",
    user_agent= "television fetch by u/Grubster11",
    )

submission = reddit.submission("xy1dai")
submission.comments.replace_more(limit=None)
comment_number = 0

with open('AllShows.json', 'r') as json_file:
    data = json.load(json_file)

    for comment in submission.comments.list():
        comment_number += 1

        # skip last weeks rankings
        if comment.author == "Grubster11":
            print("SKIP COMMENT")
            continue

        lower = comment.body.lower()
        score = comment.score
        for key, value in data.items():
            if len(key) <= 3:
                continue
            if key.lower() in lower:
                value["mentions"] += 1
                value["score"] += score
                print(key)

        if "andor" in lower and "star wars: andor" not in lower:
            data["Star Wars: Andor"]["mentions"] += 1
            data["Star Wars: Andor"]["score"] += score

        if "dahmer" in lower and "Monster: The Jeffrey Dahmer Story".lower() not in lower :
            data["Monster: The Jeffrey Dahmer Story"]["mentions"] += 1
            data["Monster: The Jeffrey Dahmer Story"]["score"] += score

        if ("she hulk" in lower or "she-hulk" in lower) and "She-Hulk: Attorney at Law".lower() not in lower:
            data["She-Hulk: Attorney at Law"]["mentions"] += 1
            data["She-Hulk: Attorney at Law"]["score"] += score

        if ("lord of the rings" in lower or "rings of power" in lower or "rop" in lower or "lotr" in lower) \
                and "The Lord of the Rings: The Rings of Power".lower() not in lower:
            data["The Lord of the Rings: The Rings of Power"]["mentions"] += 1
            data["The Lord of the Rings: The Rings of Power"]["score"] += score

        if "sandman" in lower and "The Sandman".lower() not in lower:
            data["The Sandman"]["mentions"] += 1
            data["The Sandman"]["score"] += score

        if "cyberpunk" in lower and "Cyberpunk: Edgerunners".lower() not in lower:
            data["Cyberpunk: Edgerunners"]["mentions"] += 1
            data["Cyberpunk: Edgerunners"]["score"] += score

        if ("house of dragon" in lower or "hotd" in lower or "hod" in lower) and "House of the Dragon".lower() not in lower:
            data["House of the Dragon"]["mentions"] += 1
            data["House of the Dragon"]["score"] += score

        print(comment_number)

date = datetime.today().strftime('%Y-%m-%d')

with open(f"{date}.json", 'w') as json_file:
    json_file.write(json.dumps(data))

with open(f"{date}.json", 'r') as json_file:
    data = json.load(json_file)
    df = pd.DataFrame(data)
    df = df.T
    df = df.sort_values(by=['mentions', 'score'], ascending=False)
    df.to_csv(f"{date}-mentions.csv")
    df = df.sort_values(by=['score', 'mentions'], ascending=False)
    df.to_csv(f"{date}-score.csv")











