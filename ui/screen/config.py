from . import sg, FONT_FAMILY

__title = [[sg.Text('Configurações', font=f'{FONT_FAMILY} 16 bold')]]

layout = sg.Column(
    [
        [sg.Frame('', __title, expand_x=True, element_justification='center')],
        [sg.Text('Endereço MAC:')],
        [sg.Input(key='-MAC INPUT-', disabled=True)],
        [sg.Text('Endereço do servidor:')],
        [sg.Input(key='-SERVER INPUT-')],
        [sg.Text('Senha:')],
        [sg.Input(key='-PASSWORD INPUT-')],
        [sg.Frame('', [
            [sg.Text('Motor de processamento:')],
            [sg.Radio('Classificador em Cascata', 'engine', key='-RADIO CASCADE-')],
            [sg.Radio('Tensores', 'engine', key='-RADIO TENSORS-')],
        ], expand_x=True)],
        [sg.Frame('', [[
            sg.Text('Modo de Cadastro:'), sg.Checkbox('Ativado?', tooltip='Marque para Ativar', key='-CHECK REGISTER-')
        ]], expand_x=True)],
        [sg.Frame('', [[
            sg.Text('Modo de Debug:'), sg.Checkbox('Ativado?', tooltip='Marque para Ativar', key='-CHECK DEBUG-')
        ]], expand_x=True)],
        [
            sg.Button('Cancelar', expand_x=True, font=f'{FONT_FAMILY} 16 bold',
                      key='-ROUTE-', metadata='-HOME SCREEN-'),
            sg.Button('Salvar', expand_x=True, font=f'{FONT_FAMILY} 16 bold', key='-SAVE CONFIG-')
        ],
        [sg.Button('Desligar', expand_x=True, font=f'{FONT_FAMILY} 16 bold', key='-EXIT-')]
    ], expand_y=True, expand_x=True, visible=False, key='-CONFIG SCREEN-'
)
