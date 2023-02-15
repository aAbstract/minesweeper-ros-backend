#ifndef HW_SERIAL
#define HW_SERIAL

#include <Arduino.h>

#include "./models.h"
#include "./serial_decoder.h"

// config
#define DATA_PACKET_SIZE 21

// module init
void setup_hadrware_serial() {
  Serial.begin(9600);
}

// software serial interface
void flush_hardware_serial() {
  while (Serial.available() > 0) {
    Serial.read();
  }
}

int read_hardware_serial_packet(input_serial_packet& out_input_serial_packet) {
  int data_count = 0;
  char in_buffer[128];

  while (1) {
    if (Serial.available() > 0) {
      char chr = Serial.read();

      if (chr == ';') {
        in_buffer[data_count] = 0x00;
        break;
      }

      if (chr != '\n' && chr != 13 && chr)
        in_buffer[data_count++] = chr;
    }
  }

  flush_hardware_serial();

  Serial.print("received: ");
  Serial.println(in_buffer);

  if (data_count != DATA_PACKET_SIZE)
    return 0;

  // decode serial packet
  decode_input_serial_packet(in_buffer, out_input_serial_packet);
  return 1;
}

void hw_send_data(const char* str) {
  char packet[256];
  strcpy(packet, str);
  int packet_len = strlen(packet);
  packet[packet_len] = ';';
  packet[packet_len + 1] = 0x00;
  Serial.print(packet);
}

#endif