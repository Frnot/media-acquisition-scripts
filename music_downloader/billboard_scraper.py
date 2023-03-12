import datetime
import shelve
from time import perf_counter as time

import billboard

filename = "billboard_top40"
chart_name = "pop-songs"
stop = datetime.date(2000, 1, 1)
date = datetime.date.today()

tracks = set()

with shelve.open(filename) as db:
    try:
        date = db["date"]
        tracks = db["tracks"]
    except KeyError:
        pass

while date >= stop:
    start_time = time()

    date_string = date.strftime("%Y-%m-%d")
    print(f"\nGetting date {date_string}")

    chart = billboard.ChartData(chart_name, date=date_string)

    new_entries = [(e.title, e.artist) for e in chart.entries if (e.title, e.artist) not in tracks]
    tracks.update(new_entries)

    for entry in new_entries:
        print(entry)
    print(f"total length: {len(tracks)}", end="")

    with shelve.open(filename) as db:
        db["date"] = date
        db["tracks"] = tracks
    
    end_time = time()
    print(f" | {end_time - start_time}")
    date -= datetime.timedelta(days=7)
