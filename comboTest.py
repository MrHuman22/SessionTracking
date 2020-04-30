import PySimpleGUI as sg

options = ["one", "two", "three"]
layout = [[sg.Text("Choose a category"), sg.Combo(options,key="Option")],
[sg.OK(), sg.Cancel()]
]

window = sg.Window("Test", layout)

while True:
    event, values = window.read()
    print(f"event: {event}, values: {values}")
    if event in ("OK", None, "Cancel"):
        break


window.close()