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

void PING(){
	//digitalWrite(LED_BUILTIN, HIGH);
	char msg[5] = "pong";
	talking.writeTable(msg);
	talking.endTranfert();
}

void setup(){
  Serial.begin(SERIALTALKING_BAUDRATE);
  talking.begin(Serial);

  talking.bind(0x03, PING);
}

void loop(){
  delay(1);
  talking.execute();
}