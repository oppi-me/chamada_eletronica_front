import pickle
from dataclasses import dataclass, astuple

__file_name__ = 'data.pickle'


@dataclass
class Config:
    debug: bool = True
    engine: str = 'tensors'
    server: str = 'http://localhost:5000/reconhecer',
    password: str = '1234'

    def __iter__(self):
        return iter(astuple(self))


def save(conf: Config):
    with open(__file_name__, 'wb+') as config_file:
        pickle.dump(conf, config_file, protocol=pickle.HIGHEST_PROTOCOL)


try:
    with open(__file_name__, 'rb+') as file:
        config: Config = pickle.load(file)
except FileNotFoundError:
    config = Config()
    save(config)
