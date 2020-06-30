import PySimpleGUI as sg

layout = [[sg.InputText(key='-IN-')]]
def generateLayout():
    return [[sg.InputText(key='-IN-')]

window0 = sg.Window("Base", layout)

e0, v0 = window0.read()


