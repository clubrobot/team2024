#include <Arduino.h>
#include "instructions.h"

extern AX12 ax;

//Moche mais ça marche
extern Servo servo;
/*
All the instructions are with ax.attach this is for swaping between 
differents ax12 that have differents ID
*/

void RESET(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.reset();
}

void PING_AX(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    output.write<int>(ax.ping());
}

void SET_ID(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.setID(input.read<byte>());
}

void SET_BD(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.setID(input.read<long>());
}

void MOVE(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.move(input.read<float>());
}

void MOVE_SPEED(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.moveSpeed(input.read<float>(), input.read<float>());
}

void TURN(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.turn((int) input.read<float>());
}

void SET_ENDLESS_MODE(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.setEndlessMode(input.read<bool>());
}

void SET_TEMP_LIMIT(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.setTempLimit(input.read<byte>());
}

void SET_ANGLE_LIMIT(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.setAngleLimit(input.read<float>(), input.read<float>());
}

void SET_VOLTAGE_LIMIT(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.setVoltageLimit(input.read<byte>(), input.read<byte>());
}

void SET_MAX_TORQUE(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    ax.setMaxTorque(input.read<int>());
}

void READ_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    output.write<float>(ax.readPosition());
}

void READ_SPEED(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    output.write<float>(ax.readSpeed());
}

void READ_TORQUE(SerialTalks &inst, Deserializer &input, Serializer &output){
    ax.attach(input.read<byte>());
    output.write<int>(ax.readTorque());
}

void SET_ANGLE_SERVO(SerialTalks &inst, Deserializer &input, Serializer &output){
    uint16_t angle = input.read<short>();

    servo.write(angle);
}