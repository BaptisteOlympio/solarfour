package com.cli;

import com.backend.device.ArduinoGateway;

public class Main {
    public static void main(String[] args) {
        ArduinoGateway gateway = new ArduinoGateway("/dev/ttyACM0", 9600);
        for (int i = 0; i < 50; i++) {
            gateway.sendAngle(45, 0);
        }
        gateway.close();
    }
}
