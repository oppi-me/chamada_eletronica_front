from core.detection import Detector
from core.ui import window
from core import ui
import PySimpleGUI as sg

detector = Detector(src=0).start()

ui.go2('-HOME SCREEN-')
while True:
    event, values = window.read()

    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    if 'ROUTE' in event:
        route = window.find_element(event).metadata

        if route == '-HOME SCREEN-':
            detector.start()

        if route == '-PASSWORD SCREEN-':
            detector.stop()

        ui.go2(route)

    if 'PASSWORD DIGIT' in event:
        pass

detector.release()
