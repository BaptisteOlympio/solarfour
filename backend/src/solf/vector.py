import math


class Point:
    """
    A class to manage vector operations in Cartesian and spherical coordinate systems.
    
    Coordinate system:
    - Cartesian: (x, y, z) where x points north, y points east, z points upward
    - Spherical: (azimuth, altitude) where:
        - Azimuth: angle in (x,y) plane from north (x-axis), range [0, 360) degrees
        - Altitude: elevation angle from (x,y) plane, range [-90, 90] degrees
    
    All vectors are unit vectors (magnitude = 1).
    
    Attributes:
        x (float): Cartesian x coordinate (north)
        y (float): Cartesian y coordinate (east)
        z (float): Cartesian z coordinate (up)
        azimuth (float): Azimuth angle in degrees [0, 360)
        altitude (float): Elevation angle in degrees [-90, 90]
    """

    def __init__(self, x=None, y=None, z=None, azimuth=None, altitude=None):
        """
        Initialize a Point with either Cartesian or spherical coordinates.
        
        Args:
            x (float, optional): Cartesian x coordinate
            y (float, optional): Cartesian y coordinate
            z (float, optional): Cartesian z coordinate
            azimuth (float, optional): Azimuth angle in degrees [0, 360)
            altitude (float, optional): Elevation angle in degrees [-90, 90]
        
        Raises:
            ValueError: If both or neither coordinate system is provided,
                       or if the Cartesian vector has zero magnitude.
        """
        cartesian_provided = x is not None and y is not None and z is not None
        spherical_provided = azimuth is not None and altitude is not None

        if not (cartesian_provided ^ spherical_provided):
            raise ValueError(
                "Provide either Cartesian (x, y, z) or spherical (azimuth, altitude) "
                "coordinates, not both and not neither."
            )

        if cartesian_provided:
            # Normalize to unit vector
            norm = math.sqrt(x**2 + y**2 + z**2)
            if norm == 0:
                raise ValueError("Cannot create a Point with zero magnitude.")
            
            self.x = x / norm
            self.y = y / norm
            self.z = z / norm

            # Calculate spherical coordinates
            self.azimuth = self._calculate_azimuth(self.x, self.y)
            self.altitude = self._calculate_altitude(self.x, self.y, self.z)
        else:
            # Initialize from spherical coordinates (already unit vector)
            self.azimuth = azimuth
            self.altitude = altitude

            # Convert spherical to Cartesian
            azimuth_rad = math.radians(azimuth)
            altitude_rad = math.radians(altitude)

            cos_alt = math.cos(altitude_rad)
            sin_alt = math.sin(altitude_rad)
            cos_azi = math.cos(azimuth_rad)
            sin_azi = math.sin(azimuth_rad)

            self.x = cos_alt * cos_azi
            self.y = cos_alt * sin_azi
            self.z = sin_alt

    def _calculate_azimuth(self, x, y):
        """
        Calculate azimuth in degrees [0, 360) from Cartesian coordinates.
        
        Args:
            x (float): Cartesian x coordinate
            y (float): Cartesian y coordinate
        
        Returns:
            float: Azimuth angle in degrees [0, 360)
        """
        if x == 0 and y == 0:
            return 0.0  # Undefined azimuth, default to north
        
        azi_rad = math.atan2(y, x)
        azi_deg = math.degrees(azi_rad)
        # Normalize to [0, 360) without using modulo for precision
        if azi_deg < 0.0:
            azi_deg += 360.0
        if azi_deg >= 360.0:
            azi_deg -= 360.0
        return azi_deg

    def _calculate_altitude(self, x, y, z):
        """
        Calculate altitude in degrees [-90, 90] from Cartesian coordinates.
        
        Args:
            x (float): Cartesian x coordinate
            y (float): Cartesian y coordinate
            z (float): Cartesian z coordinate
        
        Returns:
            float: Altitude (elevation) angle in degrees [-90, 90]
        """
        xy_norm = math.sqrt(x**2 + y**2)
        
        if xy_norm == 0:
            # Vector is purely vertical
            if z > 0:
                return 90.0
            elif z < 0:
                return -90.0
            else:
                return 0.0  # Zero vector (shouldn't occur for normalized vectors)
        
        alt_rad = math.atan2(z, xy_norm)
        alt_deg = math.degrees(alt_rad)
        return alt_deg

    def get_angle(self):
        """
        Get the spherical coordinates (azimuth, altitude).
        
        Returns:
            tuple: (azimuth, altitude) in degrees
        """
        return self.azimuth, self.altitude

    def get_cartesian(self):
        """
        Get the Cartesian coordinates (x, y, z).
        
        Returns:
            tuple: (x, y, z) coordinates
        """
        return self.x, self.y, self.z

    def get_opposit(self):
        """
        Get the opposite vector -v with properly normalized angles.
        
        For a vector with azimuth φ and altitude α:
        - Opposite azimuth: φ + 180, normalized to [0, 360)
        - Opposite altitude: -α
        
        Returns:
            Point: A new Point representing the opposite vector
        """
        azimuth_opp = self.azimuth + 180.0
        if azimuth_opp >= 360.0:
            azimuth_opp -= 360.0
        altitude_opp = -self.altitude
        
        return Point(azimuth=azimuth_opp, altitude=altitude_opp)

    def __repr__(self):
        return (
            f"Point(x={self.x:.6f}, y={self.y:.6f}, z={self.z:.6f}, "
            f"azimuth={self.azimuth:.2f}deg, altitude={self.altitude:.2f}deg)"
        )
