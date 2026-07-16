#include <Arduino.h>


void setup() {
    Serial.begin(9600);
}

void loop() {
    String message;
    if (Serial.available()) {
        message = Serial.readStringUntil('\n');
        char actionType = message[0];
        
        // Find the positions of the colon and comma
        int colonIndex = message.indexOf(':');
        int commaIndex = message.indexOf(',');
        
        if (colonIndex != -1 && commaIndex != -1) {
            // Extract the two numbers
            String firstNumberStr = message.substring(colonIndex + 1, commaIndex);
            String secondNumberStr = message.substring(commaIndex + 1);
            
            if (actionType == 'A') {
                float azimuth = firstNumberStr.toFloat();
                float altitude = secondNumberStr.toFloat();
                Serial.print("Turn angle : ");
                Serial.print(azimuth);
                Serial.print(",");
                Serial.println(altitude);
            } else if (actionType == 'S') {
                int step1 = firstNumberStr.toInt();
                int step2 = secondNumberStr.toInt();
                Serial.print("Turn steps: ");
                Serial.print(step1);
                Serial.print(", ");
                Serial.println(step2);
            } else {
                Serial.println("error");
            }
        } else {
            Serial.println("error: invalid format");
        }
    }
}

// #include <AccelStepper.h>

// #define STEPS_PER_REV 2048
// #define SPEED_RPM 10  // Tune here — 5 to 15 RPM is reliable for 28BYJ-48

// // Motor 1 pins: IN1, IN3, IN2, IN4
// #define M1_IN1 13
// #define M1_IN2 12
// #define M1_IN3 11
// #define M1_IN4 10

// // Motor 2 pins: IN1, IN3, IN2, IN4
// #define M2_IN1 8
// #define M2_IN2 7
// #define M2_IN3 6
// #define M2_IN4 5

// // AccelStepper expects: pin1, pin2, pin3, pin4
// AccelStepper myStepper1(AccelStepper::FULL4WIRE, M1_IN1, M1_IN3, M1_IN2, M1_IN4);
// AccelStepper myStepper2(AccelStepper::FULL4WIRE, M2_IN1, M2_IN3, M2_IN2, M2_IN4);

// // Steps per degree (2048 steps / 360 degrees for 28BYJ-48)
// #define STEPS_PER_DEGREE 5.688888

// // Serial parsing state
// #define MAX_INPUT_SIZE 64
// char inputBuffer[MAX_INPUT_SIZE];
// uint8_t inputIndex = 0;

// // Movement state
// #define PHASE_AZIMUTH 0
// #define PHASE_PAUSE 1
// #define PHASE_ALTITUDE 2
// #define PHASE_DONE 3
// uint8_t currentPhase = PHASE_DONE;
// long targetAzimuthSteps = 0;
// long targetAltitudeSteps = 0;
// unsigned long pauseStartTime = 0;

// // Motor enable state
// bool motorsEnabled = true;

// void disableStepperMotor() {
//   // Stop and disable all steppers to save power
//   myStepper1.stop();
//   myStepper2.stop();
//   myStepper1.disableOutputs();
//   myStepper2.disableOutputs();
//   motorsEnabled = false;
// }

// void enableStepperMotor() {
//   myStepper1.enableOutputs();
//   myStepper2.enableOutputs();
//   motorsEnabled = true;
// }

// void setup() {
//   Serial.begin(9600);
  
//   // Initialize all motor pins as outputs
//   pinMode(M1_IN1, OUTPUT);
//   pinMode(M1_IN2, OUTPUT);
//   pinMode(M1_IN3, OUTPUT);
//   pinMode(M1_IN4, OUTPUT);
//   pinMode(M2_IN1, OUTPUT);
//   pinMode(M2_IN2, OUTPUT);
//   pinMode(M2_IN3, OUTPUT);
//   pinMode(M2_IN4, OUTPUT);
  
//   // Convert RPM to steps/second: RPM * STEPS_PER_REV / 60
//   myStepper1.setMaxSpeed(SPEED_RPM * STEPS_PER_REV / 60.0);
//   myStepper2.setMaxSpeed(SPEED_RPM * STEPS_PER_REV / 60.0);
//   myStepper1.setAcceleration(500);
//   myStepper2.setAcceleration(500);
  
//   // Initialize buffer
//   inputBuffer[0] = '\0';
// }

// void loop() {
//   // Non-blocking serial reading
//   while (Serial.available() > 0) {
//     char received = Serial.read();
    
//     if (received == '\n') {
//       // End of line, parse the data
//       inputBuffer[inputIndex] = '\0';
      

        
//         // Enable motors if they were disabled
//         if (!motorsEnabled) {
//           enableStepperMotor();
//         }
        
//         // Convert angles to steps and store for sequential movement
//         targetAzimuthSteps = (long)(azimuthAngle * STEPS_PER_DEGREE);
//         targetAltitudeSteps = (long)(altitudeAngle * STEPS_PER_DEGREE);
        
//         // Start with azimuth phase
//         currentPhase = PHASE_AZIMUTH;
//         myStepper1.move(targetAzimuthSteps);
//         myStepper2.move(targetAzimuthSteps);
//       }
//       inputIndex = 0;
//       inputBuffer[0] = '\0';
//     } else if (inputIndex < MAX_INPUT_SIZE - 1) {
//       inputBuffer[inputIndex++] = received;
//     }
//   }

//   // Sequential movement with pause
//   if (motorsEnabled) {
//     switch (currentPhase) {
//       case PHASE_AZIMUTH:
//         myStepper1.run();
//         myStepper2.run();
//         // Check if both azimuth movements are complete
//         if (myStepper1.distanceToGo() == 0 && myStepper2.distanceToGo() == 0) {
//           currentPhase = PHASE_PAUSE;
//           pauseStartTime = millis();
//         }
//         break;
        
//       case PHASE_PAUSE:
//         // Wait for 500ms pause
//         if (millis() - pauseStartTime >= 500) {
//           currentPhase = PHASE_ALTITUDE;
//           myStepper1.move(targetAltitudeSteps);
//         }
//         break;
        
//       case PHASE_ALTITUDE:
//         myStepper1.run();
//         // Check if altitude movement is complete
//         if (myStepper1.distanceToGo() == 0) {
//           currentPhase = PHASE_DONE;
//         }
//         break;
        
//       case PHASE_DONE:
//         disableStepperMotor();
//         break;
//     }
//   }
// }