from copy import copy

import cv2
import numpy as np


def fps(image: np.ndarray, count: float):
    text = f'FPS: {round(count, 2)}'

    cv2.putText(
        image,
        text,
        (10, 25),
        cv2.FONT_HERSHEY_PLAIN,
        1.3,
        (0, 0, 0),
        6
    )
    cv2.putText(
        image,
        text,
        (10, 25),
        cv2.FONT_HERSHEY_PLAIN,
        1.3,
        (0, 255, 255),
        2
    )


def face(image, position, scale=None):
    if scale is not None:
        position = _normalized_scale(scale, position)

    rt = 1
    lt = 5
    length = 30
    color = (255, 0, 255)

    x, y, w, h = position[:4]
    width, height = x + w, y + h

    cv2.rectangle(image, position[:4], color, rt)
    # Top Left
    cv2.line(image, (x, y), (x + length, y), color, lt)
    cv2.line(image, (x, y), (x, y + length), color, lt)
    # Top Right
    cv2.line(image, (width, y), (width - length, y), color, lt)
    cv2.line(image, (width, y), (width, y + length), color, lt)
    # Bottom Left
    cv2.line(image, (x, height), (x + length, height), color, lt)
    cv2.line(image, (x, height), (x, height - length), color, lt)
    # Bottom Right
    cv2.line(image, (width, height), (width - length, height), color, lt)
    cv2.line(image, (width, height), (width, height - length), color, lt)


def probability(img, position, scale=None):
    if scale is not None:
        position = _normalized_scale(scale, position)

    cv2.putText(
        img,
        f'{int(position[-1:][0] * 100)}%',
        (position[0], position[1] - 20),
        cv2.FONT_HERSHEY_PLAIN,
        2,
        (255, 0, 255),
        2
    )


def _normalized_scale(scale, positions):
    positions = copy(positions)

    if scale > 1:
        for x in range(4):
            positions[x] = int(positions[x] * (1 * scale))

    elif scale > 0:
        for x in range(4):
            positions[x] = int(positions[x] * (1 / scale))

    else:
        raise Exception('Escala inválida.')

    return positions
