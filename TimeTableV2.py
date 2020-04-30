import PySimpleGUI as sg
from datetime import datetime, timedelta
from time import sleep
from playsound import playsound
import csv

"""
TODO: Add "extend timer option"
TODO: Track estimated times vs actual times
TODO: Add Pause and Restart Function
TODO: Set so it clears itself when a task is complete
TODO: Time remaining display
"""
def saveSession(TaskDescription, Category, Duration, TimeStart, TimeEnd):
    currentDate = datetime.strftime(TimeStart,"%Y/%m/%d")
    startTime = datetime.strftime(TimeStart, "%H:%M")
    endTime = datetime.strftime(TimeEnd, "%H:%M")
    duration = round(float(Duration)/60,2)
    actualTime = TimeEnd - TimeStart
    with open("WorkRecord.csv", "a") as fh:
        taskWriter = csv.writer(fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        taskWriter.writerow([currentDate, TaskDescription, Category, duration, startTime, endTime, actualTime])
    print("Session saved!")



class Session:
    def __init__(self, desc, duration_):
        self.started = False
        self.taskDescription = desc
        self.startTime = datetime.now()
        self.duration = float(duration_)
        self.endTime = self.startTime + timedelta(minutes=self.duration)
        self.increment = 1000 / (self.duration * 60)
        self.progress = 0

    def saveSession(self):
        pass

    def start(self):
        self.started = True
    
    def pause(self):
        self.started = False

    def incrementProgress(self):
        self.progress += self.increment

categoryOptions = sorted(["Excel Development", "Teacher Resource Development", "R&D", "Activity Development", "Show Development", "Event Management", "Misc", "3D Printing"])
sg.change_look_and_feel("Dark Blue 3")

layout = [
    [sg.Text("Task: "), sg.InputText(key='-TASK-')],
    [sg.Text("Category"), sg.Combo(categoryOptions, key = '-CATEGORY-')],
    [sg.Text("Duration: "), sg.InputText(key = '-DURATION-')],
    [sg.Text('Progress: ')],
    [sg.ProgressBar(1000,'h',size=(40,20), key='ProgressBar')],
    [sg.Button("Start"),sg.Cancel()]
]

window = sg.Window("Record Work Session", layout)
progressBar = window['ProgressBar']
# startButton = window['begin']
started = False

while True:
    event, values = window.Read(timeout=1000)
    # print(f"event: {event}, values: {values}, timerstarted?: {started}")
    
    if event == "Start":
        # # create a session
        # session = Session(values['-TASK-'],values['-DURATION-'])
        # # update the button to read pause
        # startButton.update(sg.Button("")
        mins = float(values['-DURATION-'])
        startTime = datetime.now()
        endTime = startTime + timedelta(minutes=mins)
        increments = 1000/(mins*60)
        progress = 0
        started = True
        print("starting the timer")
        currentTime = datetime.now()
    
    if started:
        if currentTime >= endTime or progress >= 1000:
            print("finished!")
            saveSession(values['-TASK-'], values['-CATEGORY-'], values['-DURATION-'], startTime, endTime)
            playsound("sms-alert-2-daniel_simon.mp3")
            sg.Popup("Go on to your next task!")
            break
        elif datetime.now() >= currentTime + timedelta(seconds=1):
            progress = progress + increments
            progressBar.UpdateBar(progress) # put in the new progress thing
            currentTime = datetime.now() # update the time
    
    if event in (None, "Cancel"):
        if not started:
            break
        if started:
            endTime = datetime.now()
            try:
                saveSession(values['-TASK-'],values['-CATEGORY-'], values['-DURATION-'], startTime, endTime)
                break
            except Exception as e:
                print(f"Errror in saving: {e}")
                break
        
window.close()

# saveSession("Test Task", "Test Category", 30, datetime(2020,4,29,5,0,0), datetime(2020,4,29,7,0,0))