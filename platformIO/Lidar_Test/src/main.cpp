#include <Arduino.h>
#include <VL53L0X.h>
#include <Wire.h>
#include <list>


#include "PIN.h"
#include "constants.h"

#include <VL53L0X.h>


using namespace std;

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
void talksExecuteWrapper()
{
    talks.execute();
    //topics.execute();
}

void setup()
{
  Serial.begin(115200);
    static int count = 0;

    // I2C Communication
    Wire.begin(SENSORS_SDA, SENSORS_SCL); //SDA SCL
    
    //bind subscription
    //topics.bind(GET_ALL_OPCODE, GET_ALL);


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
uint8_t counter;
void loop()
{
    counter = 0;

    for (const auto &cur_sensor : sensors_vl53){
        Serial.println(vl53_measurement[counter++] = cur_sensor->readRangeContinuousMillimeters());
    }
}