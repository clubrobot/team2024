#ifndef __INSTRUCTIONS_H__
#define __INSTRUCTIONS_H__

#include <SerialTalks.h>
#include <AX12.h>
#include <ESP32Servo.h>

#define RESET_OPCODE 0X12

#define PING_AX_OPCODE 0X13

#define SET_ID_OPCODE 0X14
#define SET_BD_OPCODE 0X15

#define MOVE_OPCODE 0X16
#define MOVE_SPEED_OPCODE 0X17
#define TURN_OPCODE 0x18

#define SET_ENDLESS_MODE_OPCODE 0X19

#define SET_TEMP_LIMIT_OPCODE 0X1A
#define SET_ANGLE_LIMIT_OPCODE 0X1B
#define SET_VOLTAGE_LIMIT_OPCODE 0X1C
#define SET_MAX_TORQUE_OPCODE 0X1D

#define READ_POSITION_OPCODE 0X1E
#define READ_SPEED_OPCODE 0X1F
#define READ_TORQUE_OPCODE 0X2A

#define SET_ANGLE_SERVO_OPCODE 0x2B

void RESET(SerialTalks &inst, Deserializer &input, Serializer &output);

void PING_AX(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_ID(SerialTalks &inst, Deserializer &input, Serializer &output);
void SET_BD(SerialTalks &inst, Deserializer &input, Serializer &output);

void MOVE(SerialTalks &inst, Deserializer &input, Serializer &output);
void MOVE_SPEED(SerialTalks &inst, Deserializer &input, Serializer &output);
void TURN(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_ENDLESS_MODE(SerialTalks &inst, Deserializer &input, Serializer &output);
void SET_TEMP_LIMIT(SerialTalks &inst, Deserializer &input, Serializer &output);
void SET_ANGLE_LIMIT(SerialTalks &inst, Deserializer &input, Serializer &output);
void SET_VOLTAGE_LIMIT(SerialTalks &inst, Deserializer &input, Serializer &output);
void SET_MAX_TORQUE(SerialTalks &inst, Deserializer &input, Serializer &output);

void READ_POSITION(SerialTalks &inst, Deserializer &input, Serializer &output);
void READ_SPEED(SerialTalks &inst, Deserializer &input, Serializer &output);
void READ_TORQUE(SerialTalks &inst, Deserializer &input, Serializer &output);

void SET_ANGLE_SERVO(SerialTalks &inst, Deserializer &input, Serializer &output);

#endif //__INSTRUCTIONS_H__