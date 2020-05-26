"""
This version has a persistent window
"""

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
TODO: Move debug to menu
TODO: Fix the append adding extra rows
"""

# Categories
categoryOptions = sorted(["Phone Calls", "Meetings", "Emails", "IT Helpdesk", "Excel Development", "Teacher Resource Development", "R&D", "Activity Development", "Show Development", "Event Management", "Misc", "3D Printing"])
sg.change_look_and_feel("Dark Blue 3")

menuLayout = [

]

baseLayout = [
    [sg.Button("New Session"), sg.Quit()]
]

pastdateFrameLayout = [
    [sg.T('Date: '),sg.InputText(key='-DATE-')],
    [sg.Text('Start Time: '), sg.InputText(key='-STARTTIME-')], 
    [sg.Text('End Time: '), sg.InputText(key='-ENDTIME-')]
]

metadataLayout = [
    [sg.T("Task: "), sg.InputText(key='-TASK-')],
    [sg.T("Category"), sg.Combo(categoryOptions, key = '-CATEGORY-')],
    [sg.T("Duration: "), sg.InputText(key = '-DURATION-')],
    [sg.T('Details: '), sg.InputText(key='-DETAILS-')]
]

def generateMainWindow():
    windowLayout = [
        [sg.CB("Debug Mode",key="-DEBUG-")],
        [sg.Frame("Details",metadataLayout)],
        # [sg.Text("Time remaining:"),sg.Text(0, key = 'displayTimeRemaining')],
        [sg.Frame("After the fact",pastdateFrameLayout)],
        [sg.ProgressBar(1000,'h',size=(40,20), key='ProgressBar')],
        [sg.Button('Record session',key='-LOG-',disabled=True), sg.Button("Start", key= "toggleStart", disabled=True),sg.Button("End Session", disabled=True, key="-END SESSION-"), sg.Cancel()]
    ]
    return sg.Window("Record Work Session", windowLayout)


window0 = sg.Window("Session Tracker v4.0", baseLayout)
window_active = False
window = None


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
    ev0, val0 = window0.Read(timeout = 500)
    if ev0 in (None, "Quit"):
        break
    if ev0 == "New Session" and not window_active:
        window_active = True
        window0.Hide()
        window = generateMainWindow()

        while True:
            # poll the window every 1000 ms
            event, values = window.Read(timeout = 1000)

            # Do this first or we get a sad message
            if event in (None, 'Cancel'):
                print("Quitting")
                break
            
            if values['-DEBUG-']:
                print(f"event: {event}, values: {values}")

            
        # checking and updating buttons
        
            logInfoRecorded = validLogPastSession(values['-TASK-'],values['-DURATION-'], values['-CATEGORY-'], values['-STARTTIME-'], values['-ENDTIME-'])
            window['-LOG-'].update(disabled= not logInfoRecorded) 

            if initPhase:
                if validStart(values['-CATEGORY-'],values['-DURATION-']):
                    window['toggleStart'].update(disabled=False)
                    
                if event == '-LOG-':
                    session = Session(values['-CATEGORY-'], values['-DURATION-'])
                    session.logPastSession(values['-TASK-'],values['-DETAILS-'], values['-STARTTIME-'], values['-ENDTIME-'], values['-DATE-'])
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
        window_active = False
        window.close()
        window = None
        window0.UnHide()    
window0.close()
