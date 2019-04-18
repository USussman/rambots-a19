import math

FOCAL_LENGTH = 0.0
CHORD_LENGTH = 0.0
MIRROR_HEIGHT = 0.0
CAMERA_MIRROR_HEIGHT = 0.0

MIRROR_RADIUS = MIRROR_HEIGHT/2 + CHORD_LENGTH**2/(8 * MIRROR_HEIGHT)


def distance(pixel_size):
    """
    Distance of object with fixed height.

    :param pixel_size: pixel size of object after dewarp
    :return: distance to the object in (insert units)
    """

    # TODO : determine units of distance output
    width = math.sqrt(pixel_size**2 * CAMERA_MIRROR_HEIGHT**2) / (FOCAL_LENGTH**2 - pixel_size**2)
    n =  (CHORD_LENGTH + CAMERA_MIRROR_HEIGHT) * width
    d = MIRROR_HEIGHT - MIRROR_RADIUS + math.sqrt(MIRROR_RADIUS**2 - width)
    return n / d


def distance2(pixel_size):
    width = math.sqrt(pixel_size**2 * CAMERA_MIRROR_HEIGHT**2) / (FOCAL_LENGTH**2 - pixel_size**2)
    temp = MIRROR_RADIUS**2 - (-MIRROR_HEIGHT + 2 * MIRROR_RADIUS + math.sqrt(-width**2 - MIRROR_RADIUS**2))**2
    n = width * (MIRROR_HEIGHT + math.sqrt(temp))
    d = MIRROR_HEIGHT - MIRROR_RADIUS + math.sqrt(MIRROR_RADIUS**2 - temp)
    return n / d