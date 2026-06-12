from typing import Literal

import numpy as np


def get_normal_mirror(incident_ray: np.ndarray, mirror_to_target_vector: np.ndarray):
    sum_vector = incident_ray + mirror_to_target_vector
    return (sum_vector) / np.linalg.norm(sum_vector)


def azimuth_altitude_to_cartesian(
    azimuth: float, altitude: float, angle_unit: Literal["degree", "radian"] = "degree"
):
    if angle_unit == "degree":
        azimuth = azimuth * np.pi / 180
        altitude = altitude * np.pi / 180
    x = np.cos(azimuth)
    y = np.sin(azimuth)
    z = np.sin(altitude)
    return np.array([x, y, z])
