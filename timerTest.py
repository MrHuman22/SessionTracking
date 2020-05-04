import PySimpleGUI as sg
from datetime import datetime

def getCurrentTime():
    return datetime.now()

currentTime = datetime.now()

layout = [
    [sg.Text("Current Time"), sg.Text(currentTime, key = 'timeText')],
    [sg.Text(f"Current Time {getCurrentTime()}", key = 'autoTimeText')],
    [sg.Button("Update"),sg.Cancel()]
]

window = sg.Window("Test", layout)

while True:
    event, values = window.read()
    if event in (None, "Cancel"):
        break
    elif event == "Update":
        currentTime = datetime.now()
        print(currentTime)
        window['timeText'].update(currentTime)
        window['autoTimeText'].update(f"Current Time {getCurrentTime()}")

window.close()

