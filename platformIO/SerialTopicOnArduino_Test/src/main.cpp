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
  digitalWrite(LED_BUILTIN, HIGH);
  
  talking.readTable(buffer);
  //float recv_data = talking.read<float>();
  

  //talking.addTxData(uuid);//For array
  
  talking.writeTable(buffer);
  //talking.write(recv_data);//For Values

  talking.endTranfert();//On envoie touttttt

}

void setup(){
  Serial.begin(SERIALTALKING_BAUDRATE);
  talking.begin(Serial);
}

void loop(){
  talking.execute();
}