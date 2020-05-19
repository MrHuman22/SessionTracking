from Session import Session
import PySimpleGUI as sg
from playsound import playsound
from datetime import datetime, timedelta

"""
TODO: Time remaining
TODO: Application Class refactor
TODO: Graphical display of session breakdown
TODO: Persistent Window between Sessions?
TODO: Dynamically hide/reveal session type


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
    [sg.Text('Record session after the fact:')],
    [sg.Text('Start Time: '), sg.InputText(key='-STARTTIME-')], 
    [sg.Text('End Time: '), sg.InputText(key='-ENDTIME-')],
    [sg.Button('Record session',key='-LOG-',disabled=True), sg.Button("Start", key= "toggleStart", disabled=True),sg.Button("End Session", disabled=True, key="-END SESSION-"), sg.Cancel()]
]

window = sg.Window("Record Work Session", layout)
initPhase = True
StartPause = {False : "Start", True: "Pause"}
session = None #declare global variable

def validStart(category, duration):
    return validFieldInfo(category, duration)

def validLogPastSession(task, duration, category, startTime, endTime):
    return validFieldInfo(task, duration, category, startTime, endTime)

def validEndSession(task, details):
    return validFieldInfo(task, details)

def validFieldInfo(*argv):
    """Used to record when enough information has been entered"""
    if all(map(lambda x: x != "", argv)):
        return True
    else:
        return False

#the loop
while True:
    # poll the window every 1000 ms
    event, values = window.Read(timeout = 1000)
    # print(f"event: {event}")
    # print(f"values:{values}")
   
   # checking and updating buttons
    logInfoRecorded = validLogPastSession(values['-TASK-'],values['-DURATION-'], values['-CATEGORY-'], values['-STARTTIME-'], values['-ENDTIME-'])
    window['-LOG-'].update(disabled= not logInfoRecorded) 

    if initPhase:
        if validStart(values['-CATEGORY-'],values['-DURATION-']):
            window['toggleStart'].update(disabled=False)
            
        if event == '-LOG-':
            session = Session(values['-CATEGORY-'], values['-DURATION-'])
            session.logPastSession(values['-TASK-'],values['-DETAILS-'], values['-STARTTIME-'], values['-ENDTIME-'])
            break

        if event == "toggleStart":
        # create a new session
            session = Session(values['-CATEGORY-'], values['-DURATION-'])
            window['toggleStart'].update(StartPause[session.started])
            if validEndSession(values['-TASK-'], values['-DETAILS-']):
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

        if validEndSession(values['-TASK-'], values['-DETAILS-']):
            window['-END SESSION-'].update(disabled=False)
        elif not validEndSession(values['-TASK-'], values['-DETAILS-']):
            window['-END SESSION-'].update(disabled=True)

        if event == "-END SESSION-":
            print("Ending session early...")
            session.endSession(values['-TASK-'],values['-DETAILS-'])
            break

        if event == "toggleStart":
            session.toggleStart(initPhase)
            window['toggleStart'].update(text=StartPause[session.started]) #update

    # note, if the session isn't in the started state, the progress bar doesn't progress
        if session.started:
            if session.progress >= 1000:
                print("Finished!")
                playsound("sms-alert-2-daniel_simon_short.mp3")
                sg.Popup("Go on to your next task?")
                # when signed off, save the session
                session.endSession(values['-TASK-'],values['-DETAILS-'])
                break

            elif datetime.now() >= session.currentTime + timedelta(seconds = 1):
                session.incrementProgress()
                session.updateCurrentTime()
                # print(timeRemaining)
                # window['displayTimeRemaining'].update(session.getTimeRemaining())
                # print(session.getTimeRemaining())
                window["ProgressBar"].UpdateBar(session.progress)

window.close()
