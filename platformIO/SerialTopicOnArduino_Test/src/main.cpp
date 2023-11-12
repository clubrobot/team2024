#include <Arduino.h>
#include "SerialTransfer.h"

#define SERIAL_BAUD 115200

SerialTransfer transfer;
char * s_message = (char*)"Coucou raspberry, je suis arduino.";
char r_message[255];
double y = 2.5;

struct __attribute__((packed)) STRUCT {
  char z;
  double y;
} testStruct;


void setup()
{
  // Init Serial
  Serial.begin(SERIAL_BAUD);
  transfer.begin(Serial);

  testStruct.z ='$';
  testStruct.y = 4.5;
  
}

void loop()
{
  //Envoi message
  uint16_t sendSize = 0;
  sendSize = transfer.txObj(testStruct, sendSize);
  transfer.sendData(sendSize);
  //Réception message
  /*if(transfer.available()) {
    transfer.rxObj(r_message);
    Serial.println(r_message);
  }*/

  delay(1000);
}