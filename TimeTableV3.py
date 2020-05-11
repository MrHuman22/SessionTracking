from Session import Session
import PySimpleGUI as sg
from playsound import playsound
from datetime import datetime, timedelta

"""
TODO: Time remaining
TODO: Fix button update feature
TODO: Application Class refactor
TODO: Graphical display
TODO: Persistent Window between Sessions?
"""

# Categories
categoryOptions = sorted(["Phone Calls","Meetings", "Excel Development", "Teacher Resource Development", "R&D", "Activity Development", "Show Development", "Event Management", "Misc", "3D Printing"])
sg.change_look_and_feel("Dark Blue 3")


layout = [
    [sg.Text("Task: "), sg.InputText(key='-TASK-')],
    [sg.Text("Category"), sg.Combo(categoryOptions, key = '-CATEGORY-')],
    [sg.Text("Duration: "), sg.InputText(key = '-DURATION-')],
    [sg.Text('Details: '), sg.InputText(key='-DETAILS-')],
    [sg.ProgressBar(1000,'h',size=(40,20), key='ProgressBar')],
    [sg.Text("Time remaining:"),sg.Text(0, key = 'displayTimeRemaining')],
    [sg.Button("Start", key= "toggleStart"),sg.Button("End Session", disabled=True, key="-END SESSION-"), sg.Cancel()]
]

window = sg.Window("Record Work Session", layout)
initPhase = True
StartPause = {False : "Start", True: "Pause"}
session = None #declare global variable


# the loop
while True:
    # poll the window every 1000 ms
    event, values = window.Read(timeout = 1000)
    if initPhase:
        if event == "toggleStart":
        # create a new session
            session = Session(values['-TASK-'], values['-CATEGORY-'], values['-DURATION-'])
            window['toggleStart'].update(StartPause[session.started])
            window['-END SESSION-'].update(disabled=False)
            initPhase = False #turn off input phase
            print("turning off initPhase")

        if event in (None, "Cancel"):
            print("Cancelling session. No harm done.")
            break

    elif not initPhase:
        if event in (None, "Cancel"):
            print("Session cancelled... No harm done...")
            break

        if event == "-END SESSION-":
            print("Ending session early...")
            session.endSession(values['-DETAILS-'])
            break

        if event == "toggleStart":
            session.toggleStart()
            window['begin'].update(text=StartPause[session.started]) #update

    # note, if the session isn't in the started state, the progress bar doesn't progress
        if session.started:
            if session.progress >= 1000:
                print("Finished!")
                playsound("sms-alert-2-daniel_simon_short.mp3")
                sg.Popup("Go on to your next task?")
                # when signed off, save the session
                session.endSession(values['-DETAILS-'])
                break

            elif datetime.now() >= session.currentTime + timedelta(seconds = 1):
                session.incrementProgress()
                session.updateCurrentTime()
                # print(timeRemaining)
                # window['displayTimeRemaining'].update(session.getTimeRemaining())
                # print(session.getTimeRemaining())
                window["ProgressBar"].UpdateBar(session.progress)

window.close()
