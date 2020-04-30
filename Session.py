from datetime import datetime, timedelta
import csv

class Session:
    def __init__(self, taskDescription_, category_,  duration_):
        self.started = False
        self.taskDescription = taskDescription_
        self.category = category_
        self.currentTime = datetime.now()
        self.duration = float(duration_)
        self.increment = 1000 / (self.duration * 60) # divide 1000 by the number of seconds in duration
        self.progress = 0
        self.startTime = datetime.strftime(self.currentTime, "%H:%M")
        self.currentDate = datetime.strftime(self.startTime,"%Y/%m/%d")
        self.allotedTime = timedelta(minutes = self.duration)
        self.endTime = None
        self.ellapsedTime = None
        self.timeDifference = None

    def toggleStart(self):
        self.started = not self.started

    def incrementProgress(self):
        self.progress += self.increment

    def endSession(self):
        # update all the end timings and save the session
        self.endTime = datetime.now()
        self.allotedTime = self.endTime - self.startTime
        self.ellapsedTime = self.endTime - self.startTime
        self.timeDifference = self.ellapsedTime - self.allotedTime
        self.saveSession()

    def saveSession(self):
        with open("test.csv", "a") as fh:
            writer = csv.writer(fh,delimiter=',', quotechar='"')
            writer.writerow(
                [self.currentDate, self.taskDescription, self.category, self.startTime, self.endTime, self.allotedTime, self.ellapsedTime]
                )
            print("Session Saved!")