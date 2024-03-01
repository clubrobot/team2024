/***
 * SerialTalking Lib Work In progess: CRINSA 2024
 * 
 * Negrache	Gibril et Hilkens Boris
 * 
*/

#include <Arduino.h>
#include "SerialTalking.h"


void setup(){
  Serial.begin(SERIALTALKING_BAUDRATE);
  talking.begin(Serial);
}

void loop(){
  talking.execute();
}