#include <Arduino.h>
#include "instructions.h"

extern AX12 ax;

//Moche mais ça marche
extern Servo servo1;
extern Servo servo2;
extern Servo servo3;
/*
All the instructions are with ax.attach this is for swaping between 
differents ax12 that have differents ID
*/

void RESET(){
    ax.attach(talking.read<byte>());
    ax.reset();
    talking.endTranfert();
}

void PING_AX(){
    ax.attach(talking.read<byte>());
    talking.write<byte>((ax.readVoltage()>0)?1 : 0);
    talking.endTranfert();
}

void SET_ID(){
    ax.attach(talking.read<byte>());
    ax.setID(talking.read<byte>());
    talking.endTranfert();
}

void SET_BD(){
    ax.attach(talking.read<byte>());
    ax.setID(talking.read<long>());
    talking.endTranfert();
}

void MOVE(){
    ax.attach(talking.read<byte>());
    ax.move(talking.read<float>());
    talking.endTranfert();
}

void MOVE_SPEED(){
    ax.attach(talking.read<byte>());
    ax.moveSpeed(talking.read<float>(), talking.read<float>());
    talking.endTranfert();
}

void TURN(){
    ax.attach(talking.read<byte>());
    ax.turn((int) talking.read<float>());
    talking.endTranfert();
}

void SET_ENDLESS_MODE(){
    ax.attach(talking.read<byte>());
    ax.setEndlessMode(talking.read<bool>());
    talking.endTranfert();
}

void SET_TEMP_LIMIT(){
    ax.attach(talking.read<byte>());
    ax.setTempLimit(talking.read<byte>());
    talking.endTranfert();
}

void SET_ANGLE_LIMIT(){
    ax.attach(talking.read<byte>());
    ax.setAngleLimit(talking.read<float>(), talking.read<float>());
    talking.endTranfert();
}

void SET_VOLTAGE_LIMIT(){
    ax.attach(talking.read<byte>());
    ax.setVoltageLimit(talking.read<byte>(), talking.read<byte>());
    talking.endTranfert();
}

void SET_MAX_TORQUE(){
    ax.attach(talking.read<byte>());
    ax.setMaxTorque(talking.read<int>());
    talking.endTranfert();
}

void READ_POSITION(){
    ax.attach(talking.read<byte>());
    talking.write<float>(ax.readPosition());
    talking.endTranfert();
}

void READ_SPEED(){
    ax.attach(talking.read<byte>());
    talking.write<float>(ax.readSpeed());
    talking.endTranfert();
}

void READ_TORQUE(){
    ax.attach(talking.read<byte>());
    talking.write<int>(ax.readTorque());
    talking.endTranfert();
}

void SET_ANGLE_SERVO(){
    uint16_t angle = talking.read<short>();
    uint16_t id = talking.read<short>();
    talking.endTranfert();

    switch (id)
    {
    case 1:
        servo1.write(angle);
        break;
    case 2:
        servo2.write(angle);
        break;
    case 3:
        servo3.write(angle);
        break;
    default:
        break;
    }
    
}