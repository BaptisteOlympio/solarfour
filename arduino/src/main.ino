#include <Arduino.h>
#include <AccelStepper.h>

#define STEPS_PER_REV 2048
#define SPEED_RPM 10 // Tune here — 5 to 15 RPM is reliable for 28BYJ-48
#define GEAR_RATIO 4

// Motor 1 pins: IN1, IN3, IN2, IN4
#define M1_IN1 13
#define M1_IN2 12
#define M1_IN3 11
#define M1_IN4 10

// Motor 2 pins: IN1, IN3, IN2, IN4
#define M2_IN1 8
#define M2_IN2 7
#define M2_IN3 6
#define M2_IN4 5

// AccelStepper expects: pin1, pin2, pin3, pin4
AccelStepper myStepper1(AccelStepper::FULL4WIRE, M1_IN1, M1_IN3, M1_IN2, M1_IN4);
AccelStepper myStepper2(AccelStepper::FULL4WIRE, M2_IN1, M2_IN3, M2_IN2, M2_IN4);

// Movement states
unsigned long pauseStartTime = 0;

// Motor enable state
bool motorsEnabled = true;

void setup()
{
    Serial.begin(9600);

    // Initialize all motor pins as outputs
    pinMode(M1_IN1, OUTPUT);
    pinMode(M1_IN2, OUTPUT);
    pinMode(M1_IN3, OUTPUT);
    pinMode(M1_IN4, OUTPUT);
    pinMode(M2_IN1, OUTPUT);
    pinMode(M2_IN2, OUTPUT);
    pinMode(M2_IN3, OUTPUT);
    pinMode(M2_IN4, OUTPUT);

    // Convert RPM to steps/second: RPM * STEPS_PER_REV / 60
    myStepper1.setMaxSpeed(SPEED_RPM * STEPS_PER_REV / 60.0);
    myStepper2.setMaxSpeed(SPEED_RPM * STEPS_PER_REV / 60.0);
    myStepper1.setAcceleration(500);
    myStepper2.setAcceleration(500);
}

void loop()
{
    String message;
    if (Serial.available())
    {
        message = Serial.readStringUntil('\n');
        char actionType = message[0];

        // Find the positions of the colon and comma
        int colonIndex = message.indexOf(':');
        int commaIndex = message.indexOf(',');

        if (colonIndex != -1 && commaIndex != -1)
        {
            // Extract the two numbers
            String firstNumberStr = message.substring(colonIndex + 1, commaIndex);
            String secondNumberStr = message.substring(commaIndex + 1);

            if (actionType == 'A')
            {
                float azimuth = firstNumberStr.toFloat();
                float altitude = secondNumberStr.toFloat();

                int stepAzimuth = (int)(azimuth * STEPS_PER_REV * GEAR_RATIO / 360.0);
                int stepAltitude = (int)(altitude * STEPS_PER_REV * GEAR_RATIO / 360.0);
                moveSteps(stepAzimuth, stepAzimuth);
                delay(2);
                moveSteps(0, stepAltitude);

                Serial.print("Turn angle : ");
                Serial.print(azimuth);
                Serial.print(",");
                Serial.println(altitude);
            }
            else if (actionType == 'S')
            {
                int step1 = firstNumberStr.toInt();
                int step2 = secondNumberStr.toInt();

                int resultMoveStep = moveSteps(step1, step2);

                // Confirm the move is done
                Serial.print(resultMoveStep);
                Serial.print("Turn steps: ");
                Serial.print(step1);
                Serial.print(", ");
                Serial.println(step2);
            }
            else
            {
                Serial.println("error");
            }
        }
        else
        {
            Serial.println("error: invalid format");
        }
    }
}

void disableStepperMotor()
{
    // Stop and disable all steppers to save power
    myStepper1.stop();
    myStepper2.stop();
    myStepper1.disableOutputs();
    myStepper2.disableOutputs();
    motorsEnabled = false;
}

void enableStepperMotor()
{
    myStepper1.enableOutputs();
    myStepper2.enableOutputs();
    motorsEnabled = true;
}

int angleToStep() {}

int moveSteps(int step1, int step2)
{
    // Move of the motors
    if (!motorsEnabled)
    {
        enableStepperMotor();
    }

    myStepper1.move(step1);
    myStepper2.move(step2);

    while ((myStepper1.distanceToGo() != 0) || (myStepper2.distanceToGo() != 0))
    {
        myStepper1.run();
        myStepper2.run();
    }
    disableStepperMotor();
    return 0;
}