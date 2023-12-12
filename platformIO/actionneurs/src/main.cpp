#include <Arduino.h>
#include <SerialTalking.h>
#include <AX12.h>
#include <ESP32Servo.h>
#include "PIN.h"
#include "instructions.h"

AX12 ax;

Servo servo;

void setup()
{
    //Starting SerialTalking
    Serial.begin(SERIALTALKING_BAUDRATE);
    talking.begin(Serial);

    talking.bind(RESET_OPCODE, RESET);

    talking.bind(PING_AX_OPCODE, PING_AX);

    talking.bind(SET_ID_OPCODE, SET_ID);
    talking.bind(SET_BD_OPCODE, SET_BD);

    talking.bind(MOVE_OPCODE, MOVE);
    talking.bind(MOVE_SPEED_OPCODE, MOVE_SPEED);
    talking.bind(TURN_OPCODE, TURN);

    talking.bind(SET_ENDLESS_MODE_OPCODE, SET_ENDLESS_MODE);

    talking.bind(SET_TEMP_LIMIT_OPCODE, SET_TEMP_LIMIT);
    talking.bind(SET_ANGLE_LIMIT_OPCODE, SET_ANGLE_LIMIT);
    talking.bind(SET_VOLTAGE_LIMIT_OPCODE, SET_VOLTAGE_LIMIT);
    talking.bind(SET_MAX_TORQUE_OPCODE, SET_MAX_TORQUE);

    talking.bind(READ_POSITION_OPCODE, READ_POSITION);
    talking.bind(READ_SPEED_OPCODE, READ_SPEED);
    talking.bind(READ_TORQUE_OPCODE, READ_TORQUE);

    talking.bind(SET_ANGLE_SERVO_OPCODE, SET_ANGLE_SERVO);

    //Baud, rx, tx, control
    AX12::SerialBegin(1000000, 5);

    //Servo config
    ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	ESP32PWM::allocateTimer(3);
	servo.setPeriodHertz(50);    // standard 50 hz servo
	servo.attach(PIN_SERVO2, 1000, 2000); // attaches the servo on pin 18 to the servo object
}
void loop(){ 
    talking.execute();
}