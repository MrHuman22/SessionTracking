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
        self.startTime = self.currentTime
        self.currentDate = datetime.strftime(self.currentTime,"%Y/%m/%d")
        self.allotedTime = timedelta(minutes = self.duration)
        self.scheduledEndTime = self.startTime + self.allotedTime
        self.extendTime = False
        self.endTime = None
        self.ellapsedTime = None
        self.timeDifference = None
        self.details = None
        print(f"Session begun: \nTask Description: {self.taskDescription}\nCategory: {self.category}\nAlloted Time: {self.duration}")

    def updateCurrentTime(self):
        self.currentTime = datetime.now()

    def toggleStart(self):
        self.started = not self.started
        print(f"started: {self.started}")
    
    def toggleExtend(self):
        self.extendTime = not self.extendTime
        print(f"extend time: {self.extendTime}")

    def incrementProgress(self):
        self.progress += self.increment

    def getTimeRemaining(self):
        return self.scheduledEndTime - self.currentTime 

    def endSession(self, details):
        # update all the end timings and save the session
        self.endTime = datetime.now()
        self.ellapsedTime = self.endTime - self.startTime
        self.timeDifference = self.formatTimeDiff()
        self.startTime = datetime.strftime(self.startTime,"%H:%M")
        self.endTime = datetime.strftime(self.endTime,"%H:%M")
        self.details = details
        self.saveSession()
    
    # the problem with this function is that it could be called out of sequence
    def formatTimeDiff(self):
        if self.endTime > self.scheduledEndTime:
            return (self.endTime - self.scheduledEndTime).seconds/60
        elif self.scheduledEndTime > self.endTime:
            return -(self.scheduledEndTime - self.endTime).seconds/60
        elif self.endTime == self.scheduledEndTime:
            return 0

    def saveSession(self):
        with open("test.csv", "a") as fh:
            writer = csv.writer(fh,delimiter=',', quotechar='"')
            writer.writerow(
                [self.currentDate, self.taskDescription, self.category, self.startTime, self.endTime, self.allotedTime, self.ellapsedTime, self.timeDifference, self.details]
                )
            print("Session Saved!")