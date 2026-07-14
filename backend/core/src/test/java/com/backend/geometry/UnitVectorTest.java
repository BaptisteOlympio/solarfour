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
  void shouldAngleFromCardinalCoordonate(double expectedAzimuth, double expectedAltitude, double x,
      double y, double z) {
    UnitVector v = UnitVector.fromCartesian(x, y, z);
    assertEquals(expectedAzimuth, v.getAzimuth(), DELTA,
        "Azimuth component mismatch for x=" + x + ", y=" + y + ", z=" + z);
    assertEquals(expectedAltitude, v.getAltitude(), DELTA,
        "Altitude component mismatch for x=" + x + ", y=" + y + ", z=" + z);
  }

  @Test
  void shouldAngleBetweenBisectorAndVectorsEquals() {
    UnitVector v1 = UnitVector.fromAngles(0, 90);
    UnitVector v2 = UnitVector.fromAngles(0, 0);
    UnitVector bisector = UnitVector.bisector(v1, v2);

    double angleV1ToBisectorABS = Math.acos(Math.abs(dot(v1, bisector)));
    double angleV2ToBisectorABS = Math.acos(Math.abs(dot(v2, bisector)));

    assertEquals(angleV1ToBisectorABS, angleV2ToBisectorABS, DELTA);
  }

  @Test
  void shouldReflectedRayEqualTarget() {
    UnitVector vIncident = UnitVector.fromAngles(0, 90);
    UnitVector vTarget = UnitVector.fromAngles(0, 0);
    UnitVector bisector = UnitVector.bisector(vIncident, vTarget);

    double angleVIncidentBisector = dot(vIncident, bisector);

    double xReflect = 2 * angleVIncidentBisector * bisector.getX() - vIncident.getX();
    double yReflect = 2 * angleVIncidentBisector * bisector.getY() - vIncident.getY();
    double zReflect = 2 * angleVIncidentBisector * bisector.getZ() - vIncident.getZ();

    assertEquals(vTarget.getX(), xReflect, DELTA);
    assertEquals(vTarget.getY(), yReflect, DELTA);
    assertEquals(vTarget.getZ(), zReflect, DELTA);
  }

  private static double dot(UnitVector v1, UnitVector v2) {
    return v1.getX() * v2.getX() + v1.getY() * v2.getY() + v1.getZ() * v2.getZ();
  }

  private static double norm(UnitVector v) {
    double x = v.getX(), y = v.getY(), z = v.getZ();
    return Math.sqrt(x * x + y * y + z * z);
  }
}
