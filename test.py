shows = ["The White Lotus", "The Last of Us", "The Good", "Bad"]

for show in shows:
    if show[0:4] == "The ":
        print(show)
        show = show[4:]
        print(show)
    print(show.lower())