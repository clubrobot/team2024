#include <Arduino.h>
#include "SerialTransfer.h"

#define SERIAL_BAUD 115200

#define REQUEST_BYTE 'R'
#define ANSWER_BYTE 'A'

#define PING_OPCODE 0x00
#define GETUUID_OPCODE 0x01
#define SETUUID_OPCODE 0x02
#define DISCONNECT_OPCODE 0x03
#define GETEEPROM_OPCODE 0x04
#define SETEEPROM_OPCODE  0x05
#define GETBUFFERSIZE_OPCODE 0x06

SerialTransfer transfer;
uint16_t sendSize;

/*
* Fonctions de callback
*/
void callback_ping()
{
  sendSize = 0;
  sendSize = transfer.txObj("pong.", sendSize);
  transfer.sendData(sendSize);
  //Serial.println("Test pong");
}

void callback_getuuid()
{
  sendSize = 0;
  sendSize = transfer.txObj("1234", sendSize);
  transfer.sendData(sendSize);
}

// Tableau de callbacks
const functionPtr callbackArr[] = {callback_ping, callback_getuuid};


void setup()
{
  configST myConfig;
  myConfig.debug        = true;
  myConfig.callbacks    = callbackArr;
  myConfig.callbacksLen = sizeof(callbackArr) / sizeof(functionPtr);
  
  Serial.begin(SERIAL_BAUD);
  transfer.begin(Serial,myConfig);
}

void loop()
{
  /*
  //Envoi message
  uint16_t sendSize = 0;
  sendSize = transfer.txObj(testStruct, sendSize);
  transfer.sendData(sendSize);
  //Réception message
  if(transfer.available()) {
    transfer.rxObj(r_message);
    Serial.println(r_message);
  }
  delay(1000);*/
  transfer.tick();
}