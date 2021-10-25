import threading
from threading import Thread
from time import time, sleep

import cv2
import numpy as np
import requests

from controller import ConfigController
from detection import utils, draw
from detection.cascade_classifier import CascadeClassifier
from detection.tensors import Tensors

lock = threading.Lock()


class DetectorController:
    running = False

    detector = None
    frame = None

    fps = 0
    scale = 0.5

    def __init__(self, window, config_controller, src=0, framerate=None):
        self.window = window
        self.config_controller: ConfigController = config_controller

        self.stream = cv2.VideoCapture(src)
        self.framerate = framerate

    def start(self):
        self.running = True

        if self.config_controller.config.engine == 'tensors':
            self.detector = Tensors()
        else:
            self.detector = CascadeClassifier()

        Thread(target=self.__update, args=(), daemon=True).start()
        return self

    def __update(self):
        fps_cycles = 0
        fps_start = time()
        process = 29

        while self.running:
            _, self.frame = self.stream.read()

            if self.config_controller.config.debug:
                self.__process_debug()
                self.window['-VIDEO CAPTURE DEBUG-'].update(data=utils.image2bytes(self.frame))

            elif self.config_controller.config.register:
                self.__process_register()
                self.window['-VIDEO CAPTURE REGISTER-'].update(data=utils.image2bytes(self.frame))

            else:
                process += 1
                self.frame = utils.crop(self.frame, 250, 250, center=True)
                self.window['-VIDEO CAPTURE-'].update(data=utils.image2bytes(self.frame))

                if (process % 2) == 0 and not lock.locked():
                    self.__process()

            fps_cycles += 1
            fps_end = time()
            elapsed = fps_end - fps_start
            if elapsed > 1:
                self.fps = fps_cycles / elapsed
                fps_cycles = 0
                fps_start = fps_end

            if self.framerate is not None:
                sleep((1000 / self.framerate) / 1000)

    def stop(self):
        self.running = False

    def release(self):
        self.stop()
        self.stream.release()

    def __process(self):
        frame_resized = utils.resize(self.frame, scale=self.scale)
        results = self.detector.detect(frame_resized)

        if len(results) == 1:
            Thread(target=self.__send, args=()).start()

    def __process_debug(self):
        self.frame = utils.crop(self.frame, 280, 360, center=True)
        frame_resized = utils.resize(self.frame, scale=self.scale)

        results = self.detector.detect(frame_resized)
        if len(results) > 0:
            for position in results:
                draw.face(self.frame, position, self.scale)
                if len(position) == 5:
                    draw.probability(self.frame, position, self.scale)

        draw.fps(self.frame, self.fps)

    def __process_register(self):
        self.frame = utils.crop(self.frame, 280, 320, center=True)
        frame_resized = utils.resize(self.frame, scale=self.scale)
        results = self.detector.detect(frame_resized)

        if len(results) == 1:
            self.window['-BUTTON ADD-'].update(disabled=False)
            self.window['-BUTTON SKIP-'].update(disabled=False)
            self.frame_register = np.copy(self.frame)

            for position in results:
                draw.face(self.frame, position, self.scale)

                if len(position) == 5:
                    draw.probability(self.frame, position, self.scale)

                    if position[4] > 0.93:
                        self.stop()

                else:
                    self.stop()

    def send_register(self):
        Thread(target=self.__send_register, args=()).start()

    def __send_register(self):
        self.window['-BUTTON ADD-'].update(disabled=True)
        self.window['-BUTTON SKIP-'].update(disabled=True)
        self.window['-REGISTER COMPLETED-'].update(disabled=True)

        headers = {
            'x-mac-address': self.config_controller.config.mac,
            'content-type': 'image/jpeg'
        }

        try:
            requests.post(
                self.config_controller.config.server + '/api/register',
                headers=headers,
                data=utils.image2bytes(self.frame_register, extension='.jpg')
            )
        except requests.exceptions.ConnectionError:
            pass

        self.start()
        self.window['-REGISTER COMPLETED-'].update(disabled=False)

    def __send(self):
        lock.acquire()
        self.window['-STATUS TEXT-'].update('RECONHECENDO')

        headers = {
            'x-mac-address': self.config_controller.config.mac,
            'content-type': 'image/jpeg'
        }

        try:
            r = requests.post(
                self.config_controller.config.server + '/api/recognition',
                headers=headers,
                data=utils.image2bytes(self.frame, extension='.jpg')
            )

            if r.status_code > 202:
                raise requests.exceptions.ConnectionError

            r = r.json()

            self.window['-STATUS TEXT-'].update('RECONHECIDO')
            self.window['-STUDENT NAME-'].update(r['name'])
            self.window['-STUDENT ENROLMENT-'].update(r['enrolment'])
            self.window['-STUDENT CLASS-'].update(r['class'])

            sleep(1.5)
        except requests.exceptions.ConnectionError:
            self.window['-STATUS TEXT-'].update('ERRO NA LEITURA')

            sleep(1.5)

        self.window['-STATUS TEXT-'].update('Chamada Eletrônica')
        self.window['-STUDENT NAME-'].update('')
        self.window['-STUDENT ENROLMENT-'].update('')
        self.window['-STUDENT CLASS-'].update('')

        lock.release()
