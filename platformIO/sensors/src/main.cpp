#include <Arduino.h>
#include <list>

#include "instructions.h"

#include <SerialTalking.h>

#include <Wire.h>

#include "PIN.h"
#include "constants.h"

//#include <ShiftRegister.h>
#include <VL53L0X.h>
//#include <VL6180X.h>
//#include <TaskManager.h>


using namespace std;

//TaskManager tm;

VL53L0X vl53_1 = VL53L0X(VL53L0X_1_I2C_ADDR, VL53L0X_1_SHUTDOWN_PIN, NULL);
VL53L0X vl53_2 = VL53L0X(VL53L0X_2_I2C_ADDR, VL53L0X_2_SHUTDOWN_PIN, NULL);
VL53L0X vl53_3 = VL53L0X(VL53L0X_3_I2C_ADDR, VL53L0X_3_SHUTDOWN_PIN, NULL);
VL53L0X vl53_4 = VL53L0X(VL53L0X_4_I2C_ADDR, VL53L0X_4_SHUTDOWN_PIN, NULL);
VL53L0X vl53_5 = VL53L0X(VL53L0X_5_I2C_ADDR, VL53L0X_5_SHUTDOWN_PIN, NULL);
VL53L0X vl53_6 = VL53L0X(VL53L0X_6_I2C_ADDR, VL53L0X_6_SHUTDOWN_PIN, NULL);
VL53L0X vl53_7 = VL53L0X(VL53L0X_7_I2C_ADDR, VL53L0X_7_SHUTDOWN_PIN, NULL);
VL53L0X vl53_8 = VL53L0X(VL53L0X_8_I2C_ADDR, VL53L0X_8_SHUTDOWN_PIN, NULL);

VL53L0X * sensors_vl53[] = {&vl53_1, &vl53_2, &vl53_3, &vl53_4, &vl53_5, &vl53_6, &vl53_7, &vl53_8};

uint8_t vl53_status[VL53L0X_COUNT] = {0};

uint16_t vl53_measurement[VL53L0X_COUNT] = {10};

// serialtalks wrapper
void talkingExecuteWrapper()
{
    //talking.execute();
}

void GET_ALL_SENSORS()
{
    uint8_t counter=0;
    for (const auto &cur_sensor : sensors_vl53){
        vl53_measurement[counter++] = cur_sensor->readRangeContinuousMillimeters(NULL);
    }

    talking.write<uint16_t>(vl53_measurement[0]);
    talking.write<uint16_t>(vl53_measurement[1]);
    talking.write<uint16_t>(vl53_measurement[2]);
    talking.write<uint16_t>(vl53_measurement[3]);
    talking.write<uint16_t>(vl53_measurement[4]);
    talking.write<uint16_t>(vl53_measurement[5]);
    talking.write<uint16_t>(vl53_measurement[6]);
    talking.write<uint16_t>(vl53_measurement[7]);
    talking.endTranfert();
}

void setup()
{

    static int count = 0;
    
    // Serial Communication
    Serial.begin(SERIALTALKING_BAUDRATE);
    talking.begin(Serial);
    delay(100);



    // I2C Communication
    Wire.begin(SENSORS_SDA, SENSORS_SCL); //SDA SCL
    
    // bind functions
    talking.bind(GET_ALL_SENSORS_OPCODE, GET_ALL_SENSORS);
    talking.bind(GET_SENSOR1_OPCODE, GET_SENSOR1);
    talking.bind(GET_SENSOR2_OPCODE, GET_SENSOR2);
    talking.bind(GET_SENSOR3_OPCODE, GET_SENSOR3);
    talking.bind(GET_SENSOR4_OPCODE, GET_SENSOR4);
    talking.bind(GET_SENSOR5_OPCODE, GET_SENSOR5);
    talking.bind(GET_SENSOR6_OPCODE, GET_SENSOR6);
    talking.bind(GET_SENSOR7_OPCODE, GET_SENSOR7);
    talking.bind(GET_SENSOR8_OPCODE, GET_SENSOR8);

    talking.bind(CHECK_ERROR_OPCODE, CHECK_ERROR);

    while(!talking.isConnected()){
        talking.execute();
    }


    // Shutdown all VL53L0X sensors
    for (int i=0; i<VL53L0X_COUNT; i++)
    {
        sensors_vl53[i]->shutdown();
    }
    // Set all VL53L0X timeout in ms
    for (const auto &cur_sensor : sensors_vl53)
    {
        cur_sensor->setTimeout(30);
    }
    
    // Starting all VL53L0X sensors
    for (const auto &cur_sensor : sensors_vl53)
    {
        if (!cur_sensor->begin())
        {
            vl53_status[count++] = 1;
        }
    }
    count = 0;

    // Starting all VL53L0X measure
    for (const auto &cur_sensor : sensors_vl53)
    {
        cur_sensor->startContinuous();
    }

}

// Loop

void loop(){
    //counter = 0;

    talking.execute();


}