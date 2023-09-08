#include <Arduino.h>

#include <Wire.h>

#include <ShiftRegister.h>
#include <VL53L0X.h>

VL53L0X vl53_1 = VL53L0X(0X34, 27, NULL);

void scan(){
    byte error, address;
    int nDevices;

    Serial.println("Scanning...");

    nDevices = 0;
    for (address = 1; address < 127; address++){
        // The i2c_scanner uses the return value of
        // the Write.endTransmisstion to see if
        // a device did acknowledge to the address.
        Wire.beginTransmission(address);
        error = Wire.endTransmission();

        if (error == 0)
        {
            Serial.print("I2C device found at address 0x");
            if (address < 16)
            Serial.print("0");
            Serial.print(address, HEX);
            Serial.println("  !");

            nDevices++;
        }
        else if (error == 4)
        {
            Serial.print("Unknown error at address 0x");
            if (address < 16)
                Serial.print("0");
            Serial.println(address, HEX);
        }
    }
    if (nDevices == 0)
        Serial.println("No I2C devices found\n");
    else
        Serial.println("done\n");
}
void setup(){
    Serial.begin(115200);
    
    // I2C Communication
    Wire.begin(2, 4); //SDA SCL
    delay(100);
    scan();
    delay(100);
    vl53_1.begin();
    delay(100);
    scan();
}

void loop(){
    
}