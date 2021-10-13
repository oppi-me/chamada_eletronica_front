import threading
from threading import Thread
from time import time, sleep

import cv2
import requests

from core import config
from core.config import config
from core.detection import utils, draw
from core.detection.cascade_classifier import CascadeClassifier
from core.detection.tensors import Tensors
from core.ui import window

lock = threading.Lock()


class Detector:
    def __init__(self, src=0, framerate=None):
        self.__stream = cv2.VideoCapture(src)

        self.__stopped = False

        self.__fps_framerate = framerate
        self.__fps = 0

    def start(self):
        self.__stopped = False
        Thread(target=self.__update, args=(), daemon=True).start()
        return self

    def __update(self):
        fps = 0
        fps_start = time()
        scale = 0.5
        process = 29

        if config.engine == 'tensors':
            detector = Tensors()
        else:
            detector = CascadeClassifier()

        while True:
            if self.__stopped:
                return

            ready, frame = self.__stream.read()

            if ready:
                if config.debug:
                    frame = utils.crop(frame, 280, 360, center=True)
                    frame_resized = utils.resize(frame, scale=scale)

                    results = detector.detect(frame_resized)
                    if len(results) > 0:
                        for position in results:
                            draw.face(frame, position, scale)
                            if len(position) == 5:
                                draw.probability(frame, position, scale)

                    fps += 1
                    fps_end = time()
                    if (fps_end - fps_start) > 1:
                        self.__fps = fps
                        fps = 0
                        fps_start = fps_end
                    draw.fps(frame, self.__fps)

                    window['-VIDEO CAPTURE DEBUG-'].update(data=utils.image2bytes(frame))

                else:
                    frame = utils.crop(frame, 250, 250, center=True)
                    window['-VIDEO CAPTURE-'].update(data=utils.image2bytes(frame))

                    if (process % 2) == 0 and not lock.locked():
                        lock.acquire()

                        frame_resized = utils.resize(frame, scale=scale)
                        results = detector.detect(frame_resized)

                        if len(results) > 0:
                            Thread(
                                target=_send_detection,
                                args=(frame_resized,),
                                daemon=True).start()

                    process += 1

            if self.__fps_framerate is not None:
                sleep((1000 / self.__fps_framerate) / 1000)

    def stop(self):
        self.__stopped = True

    def release(self):
        self.stop()
        self.__stream.release()


def _send_detection(image):
    try:
        headers = {'content-type': 'image/jpeg'}

        response = requests.post(
            config.server,
            data=utils.image2string(image),
            headers=headers)

        print(response)
    finally:
        lock.release()
