import numpy as np

focal_length = 0.0
chord_length = 0.0
mirror_height = 0.0
camera_mirror_height = 0.0

mirror_radius = mirror_height/2 + chord_length**2/(8 * mirror_height)

def distance(pixel_size):
    width = np.sqrt(pixel_size**2 * camera_mirror_height**2) / (focal_length**2 - pixel_size**2)
    n =  (chord_length + camera_mirror_height) * width
    d = mirror_height - mirror_radius + np.sqrt(mirror_radius**2 - width)
    return n / d

def distance2(pixel_size):
    width = np.sqrt(pixel_size**2 * camera_mirror_height**2) / (focal_length**2 - pixel_size**2)
    temp = mirror_radius**2 - (-mirror_height + 2 * mirror_radius + np.sqrt(-width**2 - mirror_radius**2))**2
    n = width * (mirror_height + np.sqrt(temp))
    d = mirror_height - mirror_radius + mp.sqrt(mirror_radius**2 - temp)
    return n / d