/***
 * SerialTalking Lib Work In progess: CRINSA 2024
 * 
 * Negrache	Gibril et Hilkens Boris
 * 
*/

#include <Arduino.h>
#include "SerialTalking.h"

/*
SerialTransfer transfer;
uint16_t sendSize;*/

/*
* Fonctions de callback
*/
/*void callback_ping(){
  uint16_t recSize = 0;
  uint16_t num = 0;
  recSize = transfer.rxObj(num, recSize);
  
  char pong[11] = {'\0'};
  sprintf(pong, "pong. %i", num);
  sendSize = 0;
  sendSize = transfer.txObj((uint16_t) sizeof(pong)/sizeof(pong[0]), sendSize); //On envoie la taille du str avant!
  sendSize = transfer.txObj(pong, sendSize, sizeof(pong)/sizeof(pong[0]));
  transfer.sendData(sendSize);
  //Serial.println("Test pong");
}*/

void callback_getuuid(){
  double recv_data[4] = {0};
  talking.receiveTransfert(recv_data);

  char uuid[] = "sensors";

  talking.addTxData(uuid);//For array
  talking.addTxDatum(recv_data[0]);//For Values
  talking.addTxDatum(recv_data[1]);//For Values
  talking.sendTranfert();//On envoie touttttt

}

void setup(){
  Serial.begin(SERIALTALKING_BAUDRATE);
  talking.begin(Serial);

  talking.bind(SERIALTALKING_PING_OPCODE, callback_getuuid);
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
  talking.execute();
}