from Session import Session
import PySimpleGUI as sg
from playsound import playsound
from datetime import datetime, timedelta

"""
TODO: Time remaining
"""

# Categories
categoryOptions = sorted(["Excel Development", "Teacher Resource Development", "R&D", "Activity Development", "Show Development", "Event Management", "Misc", "3D Printing"])
sg.change_look_and_feel("Dark Blue 3")


layout = [
    [sg.Text("Task: "), sg.InputText(key='-TASK-')],
    [sg.Text("Category"), sg.Combo(categoryOptions, key = '-CATEGORY-')],
    [sg.Text("Duration: "), sg.InputText(key = '-DURATION-')],
    [sg.Text('Details: '), sg.InputText(key='-DETAILS-')],
    [sg.ProgressBar(1000,'h',size=(40,20), key='ProgressBar')],
    [sg.Text("Time remaining:"),sg.Text(0, key = 'displayTimeRemaining')],
    [sg.Button("Start", key= "toggleStart"),sg.Button("Extend"), sg.Cancel()]
]

window = sg.Window("Record Work Session", layout)
progressBar = window['ProgressBar']
begin = window['toggleStart']
initPhase = True
StartPause = {True : "Start", False: "Pause"}
session = None #declare global variable


# the loop
while True:
    # poll the window every 1000 ms
    event, values = window.Read(timeout = 1000)
    if initPhase:
        if event == "toggleStart":
        # create a new session
            session = Session(values['-TASK-'], values['-CATEGORY-'], values['-DURATION-'])
            initPhase = False #turn off input phase
            print("turning off initPhase")

        if event in (None, "Cancel"):
            break

    elif not initPhase:
        if event in (None, "Cancel"):
            session.endSession(values['-DETAILS-'])
            break
        
        if event == "Extend":
            session.toggleExtend()

        if event == "toggleStart":
            session.toggleStart()
            begin.update(text=StartPause[session.started]) #update

    # note, if the session isn't in the started state, the progress bar doesn't progress
        
        if session.progress >= 1000:
            print("Finished!")
            playsound("sms-alert-2-daniel_simon_short.mp3")
            sg.Popup("Go on to your next task?")
            # when signed off, save the session
            session.endSession(values['-DETAILS-'])
            break

        elif datetime.now() >= session.currentTime + timedelta(seconds = 1) and not session.extendTime:
            session.incrementProgress()
            session.updateCurrentTime()
            # print(timeRemaining)
            # window['displayTimeRemaining'].update(session.getTimeRemaining())
            # print(session.getTimeRemaining())
            progressBar.UpdateBar(session.progress)

window.close()
