#include <Arduino.h>
#include "SerialTransfer.h"

#define SERIAL_BAUD 115200

SerialTransfer transfer;
char * s_message = (char*)"Coucou raspberry, je suis arduino.";
char r_message[255];

void setup()
{
  // Init Serial
  Serial.begin(SERIAL_BAUD);
  transfer.begin(Serial);
}

void loop()
{
  //Envoi message
  transfer.sendDatum(s_message);

  //Réception message
  if(transfer.available()) {
    transfer.rxObj(r_message);
    Serial.println(r_message);
  }

  delay(1000);
}