package com.backend.device;

import com.fazecast.jSerialComm.SerialPort;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.Locale;

public class ArduinoGateway {
    private final SerialPort port;
    private final OutputStream out;

    public ArduinoGateway(String portDescriptor, int baudRate) {
        this.port = SerialPort.getCommPort(portDescriptor);
        this.port.setBaudRate(baudRate);

        if (!port.openPort()) {
            throw new IllegalStateException("Could not open serial port: " + portDescriptor);
        }

        this.out = port.getOutputStream();
    }

    public void sendAngle(double azimuth, double altitude) {
        write(formatAngle(azimuth, altitude));
    }

    public void sendSteps(int step1, int step2) {
        write(formatSteps(step1, step2));
    }

    public void close() {
        port.closePort();
    }

    private String formatAngle(double azimuth, double altitude) {
        return String.format(Locale.US, "A:%.2f,%.2f%n", azimuth, altitude);
    }

    private String formatSteps(int step1, int step2) {
        return String.format(Locale.US, "S:%d,%d%n", step1, step2);
    }

    private void write(String message) {
        try {
            out.write(message.getBytes(StandardCharsets.US_ASCII));
            out.flush();
        } catch (Exception e) {
            throw new RuntimeException("Failed to write to serial port", e);
        }
    }
}
