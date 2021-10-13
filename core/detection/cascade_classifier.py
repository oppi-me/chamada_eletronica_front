import cv2

from core.config import config
from core.decorators import execution_time
from core.detection import utils


class CascadeClassifier:
    def __init__(self):
        path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.detector = cv2.CascadeClassifier(path)
        self.options = {'scaleFactor': 1.10, 'minNeighbors': 5,
                        'minSize': (30, 30), 'flags': cv2.CASCADE_SCALE_IMAGE}

    @execution_time(show=config.debug)
    def detect(self, image):
        image_gray = utils.bgr2gray(image)

        positions = self.detector.detectMultiScale(image_gray, **self.options)

        return positions
