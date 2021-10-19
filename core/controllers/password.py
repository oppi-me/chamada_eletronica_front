from core.config import config
from core.ui import window

__password = ''


def digit(x):
    global __password

    if len(__password) < 4:
        __password += x

    display = ''
    for _ in __password:
        display += '*'

    window['-PASSWORD DISPLAY-'].update(display)


def valid() -> bool:
    global __password

    return config.password == __password


def clean():
    global __password

    __password = ''

    window['-PASSWORD DISPLAY-'].update('')
