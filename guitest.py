import PySimpleGUI as sg

def generateWindow():
    layout = [[sg.Text("New window!")],[sg.InputText(key="-USER INPUT-")],[sg.OK(), sg.Cancel()]]
    return sg.Window("Session",layout)

mainLayout = [[sg.Button("New Session"),sg.Cancel()]]

window0 = sg.Window("Main", mainLayout)
window = None

while True:
    ev0, val0 = window0.Read(timeout = 1000)
    print(f"ev0: {ev0}, val0: {val0}")
    if ev0 in (None, "Cancel"):
        break
    if ev0 == "New Session":
        window0.Hide()
        window = generateWindow()
        
    
    if window != None:
        event, values = window.Read(timeout = 1000)
        print(f"event: {event}, values: {values}")

        if event in (None, "Cancel"):
            window.close()
            window = None
            window0.UnHide()
        if event == "OK":
            print(f"User input: {values['-USER INPUT-']}")
            window.close()
            window = None
            window0.UnHide()
print("Closing")
window0.close()