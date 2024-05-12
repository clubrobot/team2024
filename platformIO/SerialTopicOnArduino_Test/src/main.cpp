/***
 * SerialTalking Lib Work In progess: CRINSA 2024
 * 
 * Negrache	Gibril et Hilkens Boris
 * 
*/

#include <Arduino.h>
#include "SerialTalking.h"


int freeRam () {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}

void shit(){
  talking.write<uint16_t>((uint16_t)freeRam());
  talking.endTranfert();
}

void setup(){
  Serial.begin(SERIALTALKING_BAUDRATE);
  talking.begin(Serial);
  talking.bind(0x25, shit);
}

void loop(){
  talking.execute();
}