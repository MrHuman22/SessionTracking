import PySimpleGUI as sg
from time import sleep
from datetime import datetime, timedelta

print(datetime.now())
sg.change_look_and_feel("Dark Blue 3")

layout =  [
    [sg.Text("My Progress")],
    [sg.ProgressBar(1000,orientation='h', size = (40,20),key='progressBar')],
    [sg.Cancel()]
]

window = sg.Window('Custom Progress Meter', layout)
progress_bar = window['progressBar']
increment = 10
progress = 0

currentTime = datetime.now()
while True:
    event, values = window.Read(timeout = 100) # poll the window
    print(f"event: {event}, values: {values}")
    if event in ("Cancel", None):
        print("done!")
        break
    if datetime.now() > currentTime + timedelta(seconds=5): # every 5 seconds
        progress += increment # increase the progress
        print(f"Progress at {progress}")
        progress_bar.UpdateBar(progress)
        currentTime = datetime.now() # update timer
    if progress >= 1000:
        print("Done!")
        break

window.close()