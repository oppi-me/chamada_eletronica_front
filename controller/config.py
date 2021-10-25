import os.path
import pickle
from dataclasses import dataclass, astuple
from pathlib import Path

from controller.utils import get_mac_address

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_NAME = 'data.pickle'


@dataclass
class ConfigModel:
    debug: bool = True
    register: bool = False
    engine: str = 'tensors'
    server: str = 'http://localhost:8000'
    password: str = '1234'
    mac: str = get_mac_address()

    def __iter__(self):
        return iter(astuple(self))


class ConfigController:
    location = os.path.join(BASE_DIR, FILE_NAME)

    def __init__(self, window):
        self.window = window

        try:
            with open(self.location, 'rb+') as file:
                self.config: ConfigModel = pickle.load(file)
        except FileNotFoundError:
            self.config: ConfigModel = ConfigModel()

    def load(self):
        self.window['-MAC INPUT-'].update(self.config.mac)
        self.window['-SERVER INPUT-'].update(self.config.server)
        self.window['-PASSWORD INPUT-'].update(self.config.password)

        if self.config.debug:
            self.window['-CHECK DEBUG-'].update(True)

        if self.config.register:
            self.window['-CHECK REGISTER-'].update(True)

        if self.config.engine == 'tensors':
            self.window['-RADIO TENSORS-'].update(True)
        else:
            self.window['-RADIO CASCADE-'].update(True)

    def save(self, values):
        self.config.server = values['-SERVER INPUT-']
        self.config.password = values['-PASSWORD INPUT-']
        self.config.engine = 'tensors' if values['-RADIO TENSORS-'] else 'cascade'
        self.config.debug = values['-CHECK DEBUG-']
        self.config.register = values['-CHECK REGISTER-']

        self.dump()

    def dump(self):
        with open(self.location, 'wb+') as file:
            pickle.dump(self.config, file, protocol=pickle.HIGHEST_PROTOCOL)
