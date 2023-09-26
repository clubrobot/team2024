#include <Arduino.h>
#include "AX12.h"
// put function declarations here:


AX12 ax;


void setup() {
  // put your setup code here, to run once:
    //Baud, rx, tx, control
    Serial.begin(9600);
    AX12::SerialBegin(1000000, 5);
    ax.attach(3);
}

void loop() {
  // put your main code here, to run repeatedly:
  ax.turn(300);
  /* for(int i=0;i<254;i++){
    Serial.println(i);
    ax.attach(i);
    Serial.print("   ");
    Serial.println(ax.ping());
    delay(200);
 } */
}