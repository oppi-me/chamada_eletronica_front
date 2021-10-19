from core.config import config, save as __save
from core.ui import window


def init():
    window['-SERVER INPUT-'].update(config.server)
    window['-PASSWORD INPUT-'].update(config.password)

    if config.debug:
        window['-RADIO DEBUG1-'].update(True)
    else:
        window['-RADIO DEBUG0-'].update(True)

    if config.engine == 'tensors':
        window['-RADIO TENSORS-'].update(True)
    else:
        window['-RADIO CASCADE-'].update(True)


def save(values):
    config.server = values['-SERVER INPUT-']
    config.password = values['-PASSWORD INPUT-']
    config.engine = 'tensors' if values['-RADIO TENSORS-'] else 'cascade'
    config.debug = values['-RADIO DEBUG1-']

    __save(config)
