import requests


class LoadingController:
    def __init__(self, window, config_controller):
        while True:
            window.read(timeout=100)

            try:
                payload = {
                    'mac_address': config_controller.config.mac
                }

                r = requests.post(config_controller.config.server + '/api/ping', data=payload)
                if r.status_code > 202:
                    raise requests.exceptions.ConnectionError

                break
            except requests.exceptions.ConnectionError:
                window['-LOADING TEXT-'].update('Algo deu errado.')
                window['-LOADING INPUT-'].update(config_controller.config.server)
                window['-LOADING ERROR-'].update(visible=True)

            event, values = window.read()
            window['-LOADING TEXT-'].update('Carregando...')
            window['-LOADING ERROR-'].update(visible=False)

            config_controller.config.server = values['-LOADING INPUT-']
            config_controller.save(values)