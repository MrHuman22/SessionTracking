from datetime import datetime, timedelta
import csv

class Session:
    def __init__(self, category_,  duration_):
        self.started = True
        self.category = category_
        self.currentTime = datetime.now()
        self.duration = float(duration_)
        self.increment = 1000 / (self.duration * 60) # divide 1000 by the number of seconds in duration
        self.progress = 0
        self.startTime = self.currentTime
        self.currentDate = datetime.strftime(self.currentTime,"%Y/%m/%d")
        self.scheduledEndTime = self.startTime + timedelta(minutes=self.duration)
        self.endTime = None
        self.ellapsedTime = None
        self.allotedTime = None
        self.timeDifference = None
        self.details = None
        self.taskDescription = None
        self.pauseTime = timedelta(seconds= 0)
        self.pauseStart = None
        self.pauseEnd = None
        print(f"Session begun: \nCategory: {self.category}\nAlloted Time: {self.duration}")

    # Dealing with Pauses.
    def startPause(self):
        self.pauseStart = datetime.now()

    def endPause(self):
        self.pauseEnd = datetime.now()
        self.pauseTime += self.pauseEnd - self.pauseStart
        print(f"Cumulative pause time: {self.pauseTime}")

    def updateCurrentTime(self):
        self.currentTime = datetime.now()

    # Note, this only gets called outside of the initPhase, but the parameter is here just to make that explicit
    def toggleStart(self, initPhase):
        if not initPhase:
            if self.started:
                self.startPause()
                print("start pause")
            elif not self.started:
                self.endPause()
                print("end pause")
        self.started = not self.started
        print(f"toggled started: {self.started}")
        


    def incrementProgress(self):
        self.progress += self.increment

    def getTimeRemaining(self):
        return self.scheduledEndTime - self.currentTime 

    def endSession(self, task, details):
        # update all the end timings and save the session
        self.taskDescription = task
        self.endTime = datetime.now()
        self.ellapsedTime = round(((self.endTime - self.startTime)-self.pauseTime).seconds/60, 2)
        self.timeDifference = round(self.formatTimeDiff(),2)
        self.startTime = datetime.strftime(self.startTime,"%H:%M")
        self.endTime = datetime.strftime(self.endTime,"%H:%M")
        self.allotedTime = round(self.duration,2)
        self.details = details
        self.saveSession()

    def logPastSession(self, task, details, startTime, endTime, date = ""):
        self.taskDescription = task
        self.details = details
        self.currentDate = self.getDate(date) # possibly needs some quality control
        self.startTime = datetime.strptime(startTime,"%H:%M")
        self.endTime = datetime.strptime(endTime, "%H:%M")
        self.ellapsedTime = round((self.endTime - self.startTime).seconds/60, 2)
        self.allotedTime = round(self.duration, 2)
        self.timeDifference = "NA"
        self.startTime = datetime.strftime(self.startTime,"%H:%M")
        self.endTime = datetime.strftime(self.endTime,"%H:%M")
        self.saveSession()
    
    def getDate(self, date):
        if date == "":
            return self.currentDate
        else:
            return date
    # the problem with this function is that it could be called out of sequence
    def formatTimeDiff(self):
        if self.endTime > self.scheduledEndTime:
            return (self.endTime - self.scheduledEndTime).seconds/60
        elif self.scheduledEndTime > self.endTime:
            return -(self.scheduledEndTime - self.endTime).seconds/60
        elif self.endTime == self.scheduledEndTime:
            return 0

    def saveSession(self):
        with open("test.csv", "a",newline='') as fh:
            writer = csv.writer(fh,delimiter=',', quotechar='"')
            writer.writerow(
                [self.currentDate, self.taskDescription, self.category, self.startTime, self.endTime, self.allotedTime, self.ellapsedTime, self.timeDifference, self.details]
                )
            print("Session Saved!")