#include <Arduino.h>
//#include <SerialTalking.h>
#include <AX12.h>
#include <ESP32Servo.h>
#include "PIN.h"

AX12 ax;

Servo servo;


void setup()
{
    //Starting SerialTalking
    //Serial.begin(SERIALTALKING_BAUDRATE);
    

    //Baud, rx, tx, control
    AX12::SerialBegin(1000000, 5);

    ax.attach(254);
    ax.setEndlessMode(true);
}
void loop(){
    ax.turn(-300);
}