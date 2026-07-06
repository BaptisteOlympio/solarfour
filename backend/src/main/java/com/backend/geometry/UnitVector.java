package com.backend.geometry;

public class UnitVector {
    private float azimuth;
    private float altitude;
    private float x;
    private float y;
    private float z;

    public UnitVector(float azimuth, float altitude) {
        this.azimuth = azimuth;
        this.altitude = altitude;
    }

    public UnitVector(float x, float y, float z) {
        this.x = x;
        this.y = y;
        this.x = x;
    }
}
