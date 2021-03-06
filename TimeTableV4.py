"""
This version has a persistent window
NOTE: you can't have a layout as a global variable and reuse it
"""

from Session import Session
import PySimpleGUI as sg
from playsound import playsound
from datetime import datetime, timedelta
import pandas as pd


"""
TODO: Time remaining
TODO: Application Class refactor
TODO: Graphical display of session breakdown
TODO: Move debug to menu
TODO: Make the today's sessions prettier
TODO: Set indefinite timer
"""

# Categories
categoryOptions = sorted(["Documentation","Phone Calls", "Meetings", "Emails", "IT Helpdesk", "Excel Development", "Teacher Resource Development", "R&D", "Activity Development", "Show Development", "Event Management", "Misc", "3D Printing"])
sg.change_look_and_feel("Dark Blue 3")

def getSessionInfo():
    df = pd.read_csv("test.csv", header= 0, parse_dates= True)
    dateToday = datetime.strftime(datetime.now(), "%Y/%m/%d")
    dfFilter = df["Date"] == dateToday
    filteredDF = df[dfFilter]
    finalDF = filteredDF[["Task","Category", "Start Time", "End Time", "Description"]].to_string(justify="left")
    return finalDF


def generateMainWindow():

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

    column1Layout = [
        [sg.CB("Debug Mode",key="-DEBUG-"), sg.CB("See Today's Sessions", key = '-SHOW SESSION-')],
        [sg.Frame("Details",metadataLayout)],
        # [sg.Text("Time remaining:"),sg.Text(0, key = 'displayTimeRemaining')],
        [sg.Frame("After the fact",pastdateFrameLayout)],
        [sg.ProgressBar(1000,'h',size=(40,20), key='ProgressBar')],
        [sg.Button('Record session',key='-LOG-',disabled=True), sg.Button("Start", key= "toggleStart", disabled=True),sg.Button("End Session", disabled=True, key="-END SESSION-"), sg.Cancel()]
    ]

    column2Layout = [
        [sg.Text("Today so far:")],
        [sg.Text(getSessionInfo())]
    ]

    windowLayout = [[sg.Column(column1Layout),sg.Column(column2Layout, visible=False, key = '-SESSION COLUMN-')]]
    return sg.Window("Record Work Session", windowLayout)



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

baseLayout = [[sg.Button("New Session"), sg.Quit()]]
window0 = sg.Window("Session Tracker v4.0", baseLayout)
window = None

initPhase = True
StartPause = {False : "Start", True: "Pause"}
session = None #declare global variable

# def finish():
#     window.close()
#     window = None
#     window0.UnHide()
#     session = None
#     initPhase = True

#the loop
while True:
    ev0, val0 = window0.Read(timeout = 500)
    if ev0 in (None, "Quit"):
        break
    if ev0 == "New Session" and window == None:
        window0.Hide()
        window = generateMainWindow()

    if window != None:
            # poll the window every 1000 ms
        event, values = window.Read(timeout = 1000)

            # Do this first or we get a sad message
        if event in (None, 'Cancel'):
            print("Quitting")
            window.close()
            window = None # Destroy window
            window0.UnHide()
            continue # This makes sure that the rest of loop doesn't go forward
        
        if values['-DEBUG-']:
            print(f"event: {event}, values: {values}")

        #TODO: Don't have to keep updating if it's already been shown
        if values['-SHOW SESSION-']:
            window['-SESSION COLUMN-'].update(visible=True)
        elif not values['-SHOW SESSION-']:
            window['-SESSION COLUMN-'].update(visible=False) 
            
        # checking and updating buttons
        
        logInfoRecorded = validLogPastSession(values['-TASK-'],values['-DURATION-'], values['-CATEGORY-'], values['-STARTTIME-'], values['-ENDTIME-'])
        window['-LOG-'].update(disabled= not logInfoRecorded) 

        if initPhase:
            if validStart(values['-CATEGORY-'],values['-DURATION-']):
                window['toggleStart'].update(disabled=False)
                
            if event == '-LOG-':
                session = Session(values['-CATEGORY-'], values['-DURATION-'])
                session.logPastSession(values['-TASK-'],values['-DETAILS-'], values['-STARTTIME-'], values['-ENDTIME-'], values['-DATE-'])
                window.close()
                window = None
                window0.UnHide()
                continue

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
                window.close()
                window = None
                window0.UnHide()
                continue

        elif not initPhase:
            if event in (None, "Cancel"):
                print("Session cancelled... No harm done...")
                window.close()
                window = None
                window0.UnHide()
                initPhase = True
                continue

            if validEndSession(values['-TASK-'], values['-DETAILS-']):
                window['-END SESSION-'].update(disabled=False)
            elif not validEndSession(values['-TASK-'], values['-DETAILS-']):
                window['-END SESSION-'].update(disabled=True)

            if event == "-END SESSION-":
                print("Ending session early...")
                session.endSession(values['-TASK-'],values['-DETAILS-'])
                session = None
                window.close()
                window = None
                window0.UnHide()
                initPhase = True
                continue

            if event == "toggleStart":
                session.toggleStart(initPhase)
                window['toggleStart'].update(text=StartPause[session.started]) #update

        # note, if the session isn't in the started state, the progress bar doesn't progress
            if session != None and session.started:
                if session.progress >= 1000:
                    print("Finished!")
                    playsound("sms-alert-2-daniel_simon_short.mp3")
                    sg.Popup("Go on to your next task?")
                    # when signed off, save the session
                    session.endSession(values['-TASK-'],values['-DETAILS-'])
                    session = None # reset the session
                    window.close()
                    window = None
                    window0.UnHide()
                    continue

                elif datetime.now() >= session.currentTime + timedelta(seconds = 1):
                    session.incrementProgress()
                    session.updateCurrentTime()
                    # print(timeRemaining)
                    # window['displayTimeRemaining'].update(session.getTimeRemaining())
                    # print(session.getTimeRemaining())
                    window["ProgressBar"].UpdateBar(session.progress)    
window0.close()
