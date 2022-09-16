import os
import dotenv
import pandas as pd
import json
import praw
dotenv.load_dotenv()

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
    )

submission = reddit.submission("x9xqh4")
submission.comments.replace_more(limit=None)
comment_number = 0
for comment in submission.comments.list():
    comment_number += 1

    # skip last weeks rankings
    if comment.author == "Grubster11" or comment.author == "damnthesenames":
        print("match")
        continue
    lower = comment.body.lower()
    score = comment.score

    with open('Sept.16.22.json', 'r') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            if key.lower() in lower:
                value["mentions"] += 1
                value["score"] += score
                print(key)

        if "lord of the rings" in lower or "rings of power" in lower:
            data["The Lord of the Rings: The Rings of Power"]["mentions"] += 1
            data["The Lord of the Rings: The Rings of Power"]["score"] += score

        if "sandman" in lower:
            data["The Sandman"]["mentions"] += 1
            data["The Sandman"]["score"] += score

        if "cyberpunk" in lower:
            data["Cyberpunk: Edgerunners"]["mentions"] += 1
            data["Cyberpunk: Edgerunners"]["score"] += score

    with open('Sept.16.22.json', 'w') as json_file:
        json_file.write(json.dumps(data))

    print(comment_number)

with open('Sept.16.22.json', 'r') as json_file:
    data = json.load(json_file)
    df = pd.DataFrame(data)
    df = df.T
    df = df.sort_values(by=['mentions', 'score'], ascending=False)
    df.to_csv("Sept.16.22.csv")












