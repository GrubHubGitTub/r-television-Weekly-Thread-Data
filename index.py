import os
from dotenv import load_dotenv
import requests
import pandas as pd
import json
import praw
load_dotenv(".env")


reddit = praw.Reddit(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    password=os.getenv("password"),
    user_agent=os.getenv("user_agent"),
    username=os.getenv("username")
)


def fetch_comments(queue):
    response = requests.get(
        "https://api.pushshift.io/reddit/comment/search/?link_id=x43oq5&q=*&sort=asc&after=" + str(queue))
    response = response.json()
    comments = response["data"]
    return comments


submission = reddit.submission("x43oq5")
submission.comments.replace_more(limit=None)
comment_number = 0
for comment in submission.comments.list():
    comment_number += 1
    lower = comment.body.lower()
    score = comment.score

    with open('show_dict_copy3.json', 'r') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            if key.lower() in lower:
                value["mentions"] += 1
                if "score" not in value:
                    value["score"] = 0
                else:
                    value["score"] += score
                print(key)

        if "lord of the rings" in lower or "rings of power" in lower:
            data["The Lord of the Rings: The Rings of Power"]["mentions"] += 1
            if "score" not in data["The Lord of the Rings: The Rings of Power"]:
                value["score"] = 0
            else:
                data["The Lord of the Rings: The Rings of Power"]["score"] += score

        if "sandman" in lower:
            data["The Sandman"]["mentions"] += 1
            if "score" not in data["The Sandman"]:
                value["score"] = 0
            else:
                data["The Sandman"]["score"] += score

    with open('show_dict_copy3.json', 'w') as json_file:
        json_file.write(json.dumps(data))

    print(comment_number)

with open('show_dict_copy3.json', 'r') as json_file:
    data = json.load(json_file)
    df = pd.DataFrame(data)
    df = df.T
    df = df.sort_values(by=['mentions', 'score'], ascending=False)
    df.to_csv("shows.csv")












