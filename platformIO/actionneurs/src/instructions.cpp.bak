#include <Arduino.h>
#include "instructions.h"

extern AX12 ax;

//Moche mais ça marche
extern Servo servo;
/*
All the instructions are with ax.attach this is for swaping between 
differents ax12 that have differents ID
*/

void RESET(){
    ax.attach(talking.read<byte>());
    ax.reset();
}

void PING_AX(){
    ax.attach(talking.read<byte>());
    talking.write<int>(ax.ping());
}

void SET_ID(){
    ax.attach(talking.read<byte>());
    ax.setID(talking.read<byte>());
}

void SET_BD(){
    ax.attach(talking.read<byte>());
    ax.setID(talking.read<long>());
}

void MOVE(){
    ax.attach(talking.read<byte>());
    ax.move(talking.read<float>());
}

void MOVE_SPEED(){
    ax.attach(talking.read<byte>());
    ax.moveSpeed(talking.read<float>(), talking.read<float>());
}

void TURN(){
    ax.attach(talking.read<byte>());
    ax.turn((int) talking.read<float>());
}

void SET_ENDLESS_MODE(){
    ax.attach(talking.read<byte>());
    ax.setEndlessMode(talking.read<bool>());
}

void SET_TEMP_LIMIT(){
    ax.attach(talking.read<byte>());
    ax.setTempLimit(talking.read<byte>());
}

void SET_ANGLE_LIMIT(){
    ax.attach(talking.read<byte>());
    ax.setAngleLimit(talking.read<float>(), talking.read<float>());
}

void SET_VOLTAGE_LIMIT(){
    ax.attach(talking.read<byte>());
    ax.setVoltageLimit(talking.read<byte>(), talking.read<byte>());
}

void SET_MAX_TORQUE(){
    ax.attach(talking.read<byte>());
    ax.setMaxTorque(talking.read<int>());
}

void READ_POSITION(){
    ax.attach(talking.read<byte>());
    talking.write<float>(ax.readPosition());
}

void READ_SPEED(){
    ax.attach(talking.read<byte>());
    talking.write<float>(ax.readSpeed());
}

void READ_TORQUE(){
    ax.attach(talking.read<byte>());
    talking.write<int>(ax.readTorque());
}

void SET_ANGLE_SERVO(){
    uint16_t angle = talking.read<short>();

    servo.write(angle);
}