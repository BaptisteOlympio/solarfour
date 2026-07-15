#include <Arduino.h>

void setup() {
    Serial.begin(9600);
}

void loop() {
    Serial.println("Test");
    delay(1000);
}