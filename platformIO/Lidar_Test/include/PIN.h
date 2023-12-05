#ifndef __PIN_H__
#define __PIN_H__

#include <Arduino.h>

// Interrupt Pins

#define INTERRUPT_VL53L0X_1 16
#define INTERRUPT_VL53L0X_2 5
#define INTERRUPT_VL53L0X_3 19
#define INTERRUPT_VL53L0X_4 22
#define INTERRUPT_VL53L0X_5 13
#define INTERRUPT_VL53L0X_6 14
#define INTERRUPT_VL53L0X_7 26
#define INTERRUPT_VL53L0X_8 33

// Shutdown Shift register index
#define VL53L0X_1_SHUTDOWN_PIN 17
#define VL53L0X_2_SHUTDOWN_PIN 18
#define VL53L0X_3_SHUTDOWN_PIN 21
#define VL53L0X_4_SHUTDOWN_PIN 23
#define VL53L0X_5_SHUTDOWN_PIN 12
#define VL53L0X_6_SHUTDOWN_PIN 27
#define VL53L0X_7_SHUTDOWN_PIN 25
#define VL53L0X_8_SHUTDOWN_PIN 32

// I2C pins

#define SENSORS_SDA 2
#define SENSORS_SCL 4

// Shift register pin

#define SHIFT_REG_DATA 23
#define SHIFT_REG_CLOCK 18
#define SHIFT_REG_LATCH 19

#endif // __PIN_H__
