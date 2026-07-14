package com.backend.geometry;

public class UnitVector {
    private double azimuth;
    private double altitude;
    private double x;
    private double y;
    private double z;

    public UnitVector(double azimuth, double altitude, double x, double y, double z) {
        this.azimuth = azimuth;
        this.altitude = altitude;
        this.x = x;
        this.y = y;
        this.z = z;
    }

    public double getX() {
        return this.x;
    }

    public double getY() {
        return this.y;
    }

    public double getZ() {
        return this.z;
    }

    public double getAzimuth() {
        return this.azimuth;
    }

    public double getAltitude() {
        return this.altitude;
    }


    private static double norm(double x, double y, double z) {
        return Math.sqrt(x * x + y * y + z * z);
    }

    public static UnitVector fromCartesian(double x, double y, double z) {
        double norm = norm(x, y, z);
        double x_norm = x / norm, y_norm = y / norm, z_norm = z / norm;
        double azimuthRad;

        if (x_norm == 0.0) {
            if (y_norm > 0) {
                azimuthRad = Math.PI / 2;
            } else if (y_norm < 0) {
                azimuthRad = 3 * Math.PI / 2;
            } else {
                azimuthRad = 0.0;
            }
        } else {
            if (x_norm > 0 && y_norm >= 0) {
                azimuthRad = Math.atan(y_norm / x_norm);
            } else if (x_norm < 0 && y_norm >= 0) {
                azimuthRad = Math.PI - Math.atan(y_norm / x_norm);
            } else if (x_norm < 0 && y_norm <= 0) {
                azimuthRad = Math.PI + Math.atan(y_norm / x_norm);
            } else {
                azimuthRad = 2 * Math.PI - Math.atan(y_norm / x_norm);
            }
        }

        double azimuth = Math.toDegrees(azimuthRad);
        double altitude = Math.toDegrees(Math.asin((z_norm)));

        return new UnitVector(azimuth, altitude, x_norm, y_norm, z_norm);
    }

    public static UnitVector fromAngles(double azimuth, double altitude) {
        double azimuthRad = Math.toRadians(azimuth);
        double altitudeRad = Math.toRadians(altitude);

        double x = Math.cos(azimuthRad) * Math.cos(altitudeRad);
        double y = Math.sin(azimuthRad) * Math.cos(altitudeRad);
        double z = Math.sin(altitudeRad);
        return new UnitVector(azimuth, altitude, x, y, z);
    }

    public static UnitVector bisector(UnitVector v1, UnitVector v2) {
        return UnitVector.fromCartesian(v1.getX() + v2.getX(), v1.getY() + v2.getY(),
                v1.getZ() + v2.getZ());
    }
}
