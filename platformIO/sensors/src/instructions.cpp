#include "instructions.h"
#include "constants.h"

#include <SerialTalking.h>

extern uint16_t vl53_status[VL53L0X_COUNT];
extern uint16_t vl53_measurement[VL53L0X_COUNT];


void GET_SENSOR1()
{
    talking.write<uint16_t>(vl53_measurement[0]);
    talking.endTranfert();
}

void GET_SENSOR2()
{
    talking.write<uint16_t>(vl53_measurement[1]);
    talking.endTranfert();
}

void GET_SENSOR3()
{
    talking.write<uint16_t>(vl53_measurement[2]);
    talking.endTranfert();
}

void GET_SENSOR4()
{
    talking.write<uint16_t>(vl53_measurement[3]);
    talking.endTranfert();
}

void GET_SENSOR5()
{
    talking.write<uint16_t>(vl53_measurement[4]);
    talking.endTranfert();
}

void GET_SENSOR6()
{
    talking.write<uint16_t>(vl53_measurement[5]);
    talking.endTranfert();
}

void GET_SENSOR7()
{
    talking.write<uint16_t>(vl53_measurement[6]);
    talking.endTranfert();
}

void GET_SENSOR8()
{
    talking.write<uint16_t>(vl53_measurement[7]);
    talking.endTranfert();
}

void CHECK_ERROR()
{
    uint8_t error = 0;

    for (int i=0; i < VL53L0X_COUNT; i++)
    {
        Serial.println(vl53_status[i]);
        if (vl53_status[i] == 1)
        {
            error |= (1 << i);
        }
    }
    
    talking.write<uint8_t>(error);
    talking.endTranfert();
}