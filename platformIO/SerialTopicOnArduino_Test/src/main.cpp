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
  float recv_data = talking.read<float>();
  byte byte_data = talking.read<byte>();

  if(recv_data==5.8 && byte_data==8){
    digitalWrite(LED_BUILTIN, HIGH);
  }

  char uuid[] = "sensors";

  talking.addTxData(uuid);//For array
  talking.addTxDatum(recv_data);//For Values
  talking.addTxDatum(byte_data);//For Values

  talking.endTranfert();//On envoie touttttt

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