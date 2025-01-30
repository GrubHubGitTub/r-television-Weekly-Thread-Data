import pandas as pd
import json
import praw

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

threads = []
with open("threads.txt", "r") as file:
    Lines = file.readlines()
    for line in Lines:
        thread = line[45:52]
        threads.append(thread)
reddit = praw.Reddit(
    client_id="efvqTOiFmiUSsHiNWOquig",
    client_secret="",
    user_agent="television fetch by u/Grubster11",
)
week = 1
with open("2024-allShows.json", 'r') as json_file:
    weekly_data = json.load(json_file)

    for thread in threads:
        for show, details in weekly_data.items():
            details["mentions"] = 0
            details["score"] = 0
            details["regex-mentions"] = 0
            details["regex-score"] = 0

        print("getting")
        submission = reddit.submission(thread)
        print("thread")
        submission.comments.replace_more(limit=None)
        print("now")

        comment_number = 0
        for comment in submission.comments.list():
            comment_number += 1
            print(comment_number, comment.body)

            # skip my own comments
            import pandas as pd
            import json
            import praw
            from datetime import datetime, timedelta

            d = datetime.today()
            date = d.strftime('%d-%m-%Y')

            formatted = str(d.date())
            tup = d.fromisoformat(formatted)

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

                # some regex - it works, but undercounts due to reddit lists, line ends
                ends = [" ", "’", ",", ".", "!", "?", '"', "'", "/", ":", "&", ")", "(", "[", "]", "-", "*"]
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

        for show, details in weekly_data.items():
            details["total mentions"] +=  details["mentions"]
            details["total score"] +=  details["score"]
            details["total-regex-mentions"] += details["regex-mentions"]
            details["total-regex-score"] += details["regex-score"]

            if details["mentions"] > details["largest week amt"]:
                details["largest week amt"] = details["mentions"]

            if details["mentions"] >= 10:
                # check last weeks weekly_data and add to consecutive number
                weekly_data[show]["total top"] += 1

        print(f"done week {week}")
        week += 1

        this_week = pd.DataFrame(weekly_data)
        this_week = this_week.T
        this_week.index.name = 'name'
        this_week = this_week[~(this_week.index.str.len() < 4)]
        skip_shows = ["Ally", "Really", "Star", "King", "From", "FROM","Will","Brot", "Time", "Arte", "The First", "The Show", "Bette",
                      "Last",
                      "Next", "neXt", "Don't", "Them", "Hile", "Vera", "Drama", "The Story", "Stat", "Before",
                      "Another", "Roba", "Back", "Hard", "Haven", "Made", "High", "Look", "Episodes", "Hank",
                      "Times",
                      "Land", "Ellen", "Action", "Rise", "Found", "Between", "Mila", "Help", "Sever", "Thanks",
                      "The End",
                      "Looking", "Live", "Life", "LIFE", "Origin", "Else", "Girls", "GIRLS", "Absolutely",
                      "Special", "Lace",
                      "Together", "ToGetHer", "Love", "Dark", "VICE", "Itch", "Anno", "Stone", "Honest", "Kings",
                      "The Great Show",
                      "The Game", "Television"]
        this_week = this_week[~this_week.index.isin(skip_shows)]

        this_week = this_week.sort_values(by=['total mentions', 'total score'], ascending=False)
        this_week.to_csv(f"2024-cleaned.csv")

    this_week = pd.DataFrame(weekly_data)
    this_week = this_week.T
    this_week.index.name = 'name'
    this_week = this_week[~(this_week.index.str.len() < 4)]
    skip_shows = ["Ally", "Really", "Star", "King", "From", "Time", "Arte", "The First", "The Show", "Bette",
                  "Last",
                  "Next", "neXt", "Don't", "Them", "Hile", "Vera", "Drama", "The Story", "Stat", "Before",
                  "Another", "Roba", "Back", "Hard", "Haven", "Made", "High", "Look", "Episodes", "Hank",
                  "Times",
                  "Land", "Ellen", "Action", "Rise", "Found", "Between", "Mila", "Help", "Sever", "Thanks",
                  "The End",
                  "Looking", "Live", "Life", "LIFE", "Origin", "Else", "Girls", "GIRLS", "Absolutely",
                  "Special", "Lace",
                  "Together", "ToGetHer", "Love", "Dark", "VICE", "Itch", "Anno", "Stone", "Honest", "Kings",
                  "The Great Show",
                  "The Game", "Television"]
    this_week = this_week[~this_week.index.isin(skip_shows)]

    this_week = this_week.sort_values(by=['mentions', 'score'], ascending=False)
    this_week.to_csv(f"2024-cleaned.csv")
