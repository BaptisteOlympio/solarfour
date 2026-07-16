package com.cli;

import com.backend.device.ArduinoGateway;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        ArduinoGateway gateway = new ArduinoGateway("/dev/ttyACM0", 9600);
        Scanner userInputScanner = new Scanner(System.in);

        while (true) {
            System.out.println("Enter mode : angle/steps/close");
            String modeInput = userInputScanner.nextLine();
            if (modeInput.equals("angle")) {
                System.out.println("Enter angle : <azimuth,altitude>");
                String angleInput = userInputScanner.nextLine();
                Double angles[] = extractStringToDouble(angleInput);
                Double azimuth = angles[0];
                Double altitude = angles[1];
                gateway.sendAngle(azimuth, altitude);
                System.out.println("Angle send : " + angleInput);
            } else if (modeInput.equals("steps")) {
                System.out.println("Enter steps : <step1,step2>");
                String stepsInput = userInputScanner.nextLine();
                int steps[] = extractStringToInt(stepsInput);
                int step1 = steps[0];
                int step2 = steps[1];
                gateway.sendSteps(step1, step2);
            } else if (modeInput.equals("close")) {
                break;
            } else {
                System.out.println("Wrong mode");
            }
        }
        System.out.println("Closing connection...");
        gateway.close();
        userInputScanner.close();
        System.out.println("Connection closed");
    }

    public static Double[] extractStringToDouble(String message) {
        Double values[] = new Double[2];
        String[] splitMessage = message.split(",");
        values[0] = Double.parseDouble(splitMessage[0]);
        values[1] = Double.parseDouble(splitMessage[1]);
        return values;
    }

    public static int[] extractStringToInt(String message) {
        int values[] = new int[2];
        String[] splitMessage = message.split(",");
        values[0] = Integer.parseInt(splitMessage[0]);
        values[1] = Integer.parseInt(splitMessage[1]);
        return values;
    }
}
