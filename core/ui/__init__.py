from core.config import config
from .screens.debug import layout as debug
from .screens.home import layout as home
from .screens.password import layout as password
from .utils import sg

layout = [[
    debug,
    home,
    password
]]

window = sg.Window(
    'Chamada Eletrônica',
    layout,
    finalize=True,
    grab_anywhere=True,
    # location=(0, 0),
    # margins=(2, 2),
    # no_titlebar=True,
    size=(320, 480)
)

screens = ['-DEBUG SCREEN-', '-HOME SCREEN-', '-PASSWORD SCREEN-']


def go2(route):
    for screen in screens:
        window[screen].update(visible=False)

    if config.debug and route == '-HOME SCREEN-':
        window['-DEBUG SCREEN-'].update(visible=True)
    else:
        window[route].update(visible=True)
