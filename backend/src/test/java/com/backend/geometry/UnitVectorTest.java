package com.backend.geometry;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class UnitVectorTest {
    private static final double DELTA = 1e-6;

    @Test
    void shouldHaveUnitNorm_whenCreatedFromCartesian() {
        UnitVector v = UnitVector.fromCartesian(30, -45, 10);
        assertEquals(1.0, norm(v), DELTA, "Cartesian vector must be normalized");
    }

    @Test
    void shouldHaveUnitNorm_whenCreatedFromAngles() {
        UnitVector v = UnitVector.fromAngles(45.0, 90.0);
        assertEquals(1.0, norm(v), DELTA, "Angle-based vector must be normalized");
    }

    @ParameterizedTest
    @CsvSource({"0,   0,  1,  0,  0", // North
            "90,  0,  0,  1,  0", // West
            "180, 0, -1,  0,  0", // South
            "270, 0,  0, -1,  0", // East
            "0,   90, 0,  0,  1" // Zenith
    })
    void shouldPointInCardinalDirection(double azimuth, double altitude, double expectedX,
            double expectedY, double expectedZ) {
        UnitVector v = UnitVector.fromAngles(azimuth, altitude);
        assertEquals(expectedX, v.getX(), DELTA,
                "X component mismatch for azimuth=" + azimuth + ", altitude=" + altitude);
        assertEquals(expectedY, v.getY(), DELTA,
                "Y component mismatch for azimuth=" + azimuth + ", altitude=" + altitude);
        assertEquals(expectedZ, v.getZ(), DELTA,
                "Z component mismatch for azimuth=" + azimuth + ", altitude=" + altitude);
    }

    @ParameterizedTest
    @CsvSource({"0,   0,  1,  0,  0", // North
            "90,  0,  0,  1,  0", // West
            "180, 0, -1,  0,  0", // South
            "270, 0,  0, -1,  0", // East
            "0,   90, 0,  0,  1" // Zenith
    })
    void shouldAngleFromCardinalCoordonate(double expectedAzimuth, double expectedAltitude,
            double x, double y, double z) {
        UnitVector v = UnitVector.fromCartesian(x, y, z);
        assertEquals(expectedAzimuth, v.getAzimuth(), DELTA,
                "Azimuth component mismatch for x=" + x + ", y=" + y + ", z=" + z);
        assertEquals(expectedAltitude, v.getAltitude(), DELTA,
                "Altitude component mismatch for x=" + x + ", y=" + y + ", z=" + z);
    }

    private static double norm(UnitVector v) {
        double x = v.getX(), y = v.getY(), z = v.getZ();
        return Math.sqrt(x * x + y * y + z * z);
    }
}
