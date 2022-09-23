import os
import dotenv
import pandas as pd
import json
import praw
dotenv.load_dotenv()

reddit = praw.Reddit(
    client_id=,
    client_secret=,
    user_agent=,
    )

submission = reddit.submission("xftnak")
submission.comments.replace_more(limit=None)
comment_number = 0

with open('AllShows.json', 'r') as json_file:
    data = json.load(json_file)

    for comment in submission.comments.list():
        comment_number += 1

        # skip last weeks rankings
        if comment.author == "Grubster11" or comment.author == "damnthesenames":
            print("SKIP COMMENT")
            continue
        lower = comment.body.lower()
        score = comment.score

        for key, value in data.items():
            if key.lower() in lower:
                value["mentions"] += 1
                value["score"] += score
                print(key)

        if "dahmer" in lower:
            data["Monster: The Jeffrey Dahmer Story"]["mentions"] += 1
            data["Monster: The Jeffrey Dahmer Story"]["score"] += score

        if "she hulk" in lower or "she-hulk" in lower:
            data["She-Hulk: Attorney at Law"]["mentions"] += 1
            data["She-Hulk: Attorney at Law"]["score"] += score

        if "lord of the rings" in lower or "rings of power" in lower:
            data["The Lord of the Rings: The Rings of Power"]["mentions"] += 1
            data["The Lord of the Rings: The Rings of Power"]["score"] += score

        if "sandman" in lower:
            data["The Sandman"]["mentions"] += 1
            data["The Sandman"]["score"] += score

        if "cyberpunk" in lower:
            data["Cyberpunk: Edgerunners"]["mentions"] += 1
            data["Cyberpunk: Edgerunners"]["score"] += score

        if "house of dragon" in lower:
            data["House of the Dragon"]["mentions"] += 1
            data["House of the Dragon"]["score"] += score

        print(comment_number)

with open('Sept.23.22.json', 'w') as json_file:
    json_file.write(json.dumps(data))

with open('Sept.23.22.json', 'r') as json_file:
    data = json.load(json_file)
    df = pd.DataFrame(data)
    df = df.T
    df = df.sort_values(by=['mentions', 'score'], ascending=False)
    df.to_csv("Sept.23.22.csv")












