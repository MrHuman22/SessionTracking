import csv
from datetime import datetime, timedelta

with open("test.csv", "a") as fh:
    csvWriter = csv.writer(fh,delimiter= ',')
    csvWriter.writerow(["Task", "Start Time", "End Time"])
    csvWriter.writerow(["Set up timer properly", datetime.now(), datetime.now()+timedelta(minutes=1)])