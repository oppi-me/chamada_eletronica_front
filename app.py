import PySimpleGUI as sg

from core import ui
import core.controllers as controller
from core.detection import Detector
from core.ui import window

detector = Detector(src=0).start()

controller.config.init()
ui.go2('-HOME SCREEN-')
while True:
    event, values = window.read()

    if event == '-EXIT-' or event == sg.WIN_CLOSED:
        break

    if 'ROUTE' in event:
        route = window.find_element(event).metadata

        if route == '-HOME SCREEN-':
            detector.start()
            controller.password.clean()

        if route == '-PASSWORD SCREEN-':
            detector.stop()

        if route == '-CONFIG SCREEN-':
            if not controller.password.valid():
                controller.password.clean()
                continue

        ui.go2(route)

    if 'PASSWORD DIGIT' in event:
        controller.password.digit(window.find_element(event).metadata)

    if event == '-SAVE CONFIG-':
        controller.config.save(values)
        controller.password.clean()
        detector.start()
        ui.go2('-HOME SCREEN-')

detector.release()
