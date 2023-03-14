from datetime import datetime, timedelta
import json
d = datetime.today()
date = d.strftime('%d-%m-%Y')

for i in range(5,12):
    last_week_date = (d - timedelta(days=i)).strftime('%d-%m-%Y')
    try:
        with open(f"{last_week_date}-allShows.json", 'r') as json_file:
            last_week = json.load(json_file)
            print("ya", {last_week_date})
            break
    except FileNotFoundError:
        pass
print(last_week)