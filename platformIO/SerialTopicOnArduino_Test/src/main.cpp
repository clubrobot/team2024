/***
 * SerialTalking Lib Work In progess: CRINSA 2024
 * 
 * Negrache	Gibril et Hilkens Boris
 * 
*/

#include <Arduino.h>
#include "SerialTalking.h"
char buffer[50] ={0};

void callback_getuuid(){

  talking.readTable(buffer);
  float recv_data = talking.read<float>();
  

  //talking.addTxData(uuid);//For array
  
  talking.writeTable(buffer);
  talking.write(recv_data);//For Values

  talking.endTranfert();//On envoie touttttt

}

void setup(){
  Serial.begin(SERIALTALKING_BAUDRATE);
  talking.begin(Serial);

  talking.bind(SERIALTALKING_PING_OPCODE, callback_getuuid);
}

void loop(){

  talking.execute();
}