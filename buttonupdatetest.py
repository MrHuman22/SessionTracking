import PySimpleGUI as sg

layout = [[sg.Button('Start',key='toggleStart'), sg.Cancel()]]

window = sg.Window("Test Update", layout)
begin = window['toggleStart']
StartPause = {True : "Start", False : "Pause"}
Started = True

while True:
    event, values = window.Read(timeout = 1000)
    print(f"event: {event}, values: {values}")
    if event in (None, "Cancel"):
        break
    elif event == "toggleStart":
        Started = not Started
        begin.update(text=StartPause[Started])
        sg.Popup("Things have changed!")

window.close()