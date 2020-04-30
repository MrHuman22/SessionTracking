import PySimpleGUI as sg
from datetime import datetime, timedelta
from time import sleep
from playsound import playsound
import csv

"""
TODO: Set up progress bar
TODO: Work out how to have the program NOT sit there and wait. Threading?
TODO: Write the date timestamp and time timestamps in different columns
TODO: Have an interupt in case something doesn't take as long as I thought
"""
categoryOptions = sorted(["Excel Development", "Teacher Resource Development", "R&D", "Activity Development", "Show Development", "Event Management"])
sg.change_look_and_feel("Dark Blue 3")

layout = [
    [sg.Text("Task: "), sg.InputText(key='-TASK-')],
    [sg.Combo(categoryOptions, key = '-CATEGORY-')],
    [sg.Text("Duration: "), sg.InputText(key = '-DURATION-')],
    [sg.Button("Start"),sg.Cancel()]
    ]

window = sg.Window("Timetable",layout)
while True:
    event, values = window.read()
    print(f"Event: {event}, values: {values}")
    if event in (None, "Cancel", "Exit"):
        break
    if event == 'OK':
        if "-DURATION-" in values.keys():
            mins = int(values["-DURATION-"])
            startTime = datetime.now()
            endTime = startTime + timedelta(minutes=mins)
            print(f"You'll be alerted at {endTime}")
            while datetime.now() < endTime:
                sleep(10) # don't check all the time
                if datetime.now() >= endTime:
                    print("Now!")
                    playsound("sms-alert-2-daniel_simon.mp3")
                    sg.Popup("Time to move on to your next task!")
                    window.close()
                    with open("WorkRecord.csv", "a") as fh:
                        taskWriter = csv.writer(fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        taskWriter.writerow([values['-TASK-'], values['-CATEGORY-'], values['-DURATION-'], startTime, endTime])
                    break
 
window.close()

