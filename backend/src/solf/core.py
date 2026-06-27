from typing import Literal, Union
from datetime import datetime

from pysolar.solar import get_altitude_fast, get_azimuth_fast
from pytz import timezone
import numpy as np

from .vector import Point


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

def get_azimuth_altitide(latitude_deg, longitude_deg, date: Union[Literal["now"], datetime], time_zone=timezone("Europe/Paris")):
    if date == "now":
        date = datetime.now(time_zone)

    altitude = get_altitude_fast(
        latitude_deg=latitude_deg, longitude_deg=longitude_deg, when=date
    )
    azimuth = get_azimuth_fast(
        latitude_deg=latitude_deg, longitude_deg=longitude_deg, when=date
    )
    return azimuth, altitude


def add(point1: Point, point2: Point) -> Point:
    """
    Add two Point vectors and return the normalized sum.
    
    The sum is computed in Cartesian space (x, y, z) and then normalized
    to a unit vector through the Point constructor.
    
    Args:
        point1: First Point vector
        point2: Second Point vector
    
    Returns:
        Point: A new Point representing the normalized sum of the two vectors
    """
    x_sum = point1.x + point2.x
    y_sum = point1.y + point2.y
    z_sum = point1.z + point2.z
    return Point(x=x_sum, y=y_sum, z=z_sum)


def get_delta_angles(point1: Point, point2: Point) -> tuple[float, float]:
    """
    Calculate the delta angles (delta_azimuth, delta_altitude) to go from point1 to point2.
    
    Args:
        point1: Starting Point
        point2: Target Point
    
    Returns:
        tuple: (delta_azimuth, delta_altitude) in degrees
    """
    delta_azimuth = point2.azimuth - point1.azimuth
    delta_altitude = point2.altitude - point1.altitude
    return delta_azimuth, delta_altitude
