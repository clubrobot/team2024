#include <Arduino.h>
#include <EEPROM.h>

void setup() {
  Serial.begin(9600);
  for (int i = 0 ; i < 512 ; i++) {
    unsigned char val = EEPROM.read(i);
    Serial.print("-");
    Serial.print(i);
    Serial.print("-");
    Serial.println(val);
  }
  
    for (int i = 0 ; i < 512 ; i++) {
      EEPROM.write(i, 0XFF);
  }
  
    for (int i = 0 ; i < 512 ; i++) {
    unsigned char val = EEPROM.read(i);
    Serial.print("-");
    Serial.print(i);
    Serial.print("-");
    Serial.println(val);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
}