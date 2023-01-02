from datetime import datetime, timedelta

d = datetime.today()
date = str(d.date())
tu = d.fromisoformat(date)
w = datetime.date(tu).isocalendar()[1]
print(w)
