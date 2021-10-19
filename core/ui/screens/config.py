from core.ui.utils import FONT_FAMILY
from core.ui.utils import sg

__title = [[sg.Text('Configurações', font=f'{FONT_FAMILY} 16 bold')]]

layout = sg.Column(
    [
        [sg.Frame('', __title, expand_x=True, element_justification='center')],
        [sg.Text('Endereço do servidor:')],
        [sg.Input(key='-SERVER INPUT-')],
        [sg.Text('Senha:')],
        [sg.Input(key='-PASSWORD INPUT-')],
        [sg.Frame('', [
            [sg.Text('Motor de processamento:')],
            [sg.Radio('Classificador em Cascata', 'engine', key='-RADIO CASCADE-')],
            [sg.Radio('Tensores', 'engine', key='-RADIO TENSORS-')],
        ], expand_x=True)],
        [sg.Frame('', [
            [sg.Text('Modo Debug:')],
            [
                sg.Radio('Ativar', 'debug', key='-RADIO DEBUG1-', size=(12, 1)),
                sg.Radio('Desativar', 'debug', key='-RADIO DEBUG0-', size=(12, 1))
            ],
        ], expand_x=True)],
        [
            sg.Button('Cancelar', expand_x=True, font=f'{FONT_FAMILY} 16 bold',
                      key='-ROUTE-', metadata='-HOME SCREEN-'),
            sg.Button('Salvar', expand_x=True, font=f'{FONT_FAMILY} 16 bold', key='-SAVE CONFIG-')
        ],
        [sg.Button('Desligar', expand_x=True, font=f'{FONT_FAMILY} 16 bold', key='-EXIT-')]
    ], expand_y=True, expand_x=True, visible=False, key='-CONFIG SCREEN-'
)
