#ifndef MOTORS
#define MOTORS

#include <Arduino.h>

#include "./Adafruit_MCP4725.h"

// Motors Control
uint32_t dac_value = 0;
uint32_t dac2_value = 0;
int data;
Adafruit_MCP4725 dac;
Adafruit_MCP4725 dac2;

// MOTORS MOTION
void zero() {
  dac_value = 2048;
  dac.setVoltage(dac_value, false);
  dac2_value = 2048;
  dac2.setVoltage(dac2_value, false);
}

void forward() {
  dac_value = 2048;
  dac.setVoltage(dac_value, false);
  dac2_value = 0;
  dac2.setVoltage(dac2_value, false);
}

void backward() {
  dac_value = 2048;
  dac.setVoltage(dac_value, false);
  dac2_value = 4095;
  dac2.setVoltage(dac2_value, false);
}

void left() {
  dac_value = 0;
  dac.setVoltage(dac_value, false);
  dac2_value = 2048;
  dac2.setVoltage(dac2_value, false);
}

void right() {
  dac_value = 4095;
  dac.setVoltage(dac_value, false);
  dac2_value = 2048;
  dac2.setVoltage(dac2_value, false);
}

#endif
