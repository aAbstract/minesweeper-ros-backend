#ifndef SW_SERIAL
#define SW_SERIAL

#include <Arduino.h>
#include <SoftwareSerial.h>

// config
#define SER_RX_PIN 8
#define SER_TX_PIN 9
#define SER_TIME_OUT 10

// state
SoftwareSerial software_serial(SER_RX_PIN, SER_TX_PIN);

// module init
void setup_software_serial() {
  software_serial.begin(9600);
}

// software serial interface
void flush_software_serial() {
  while (software_serial.available() > 0) {
    software_serial.read();
  }
}

int read_software_serial(char* out_buffer) {
  int data_count = 0;
  int time_out_count = 0;

  while (1) {
    if (software_serial.available() > 0) {
      char chr = software_serial.read();

      if (chr == ';') {
        out_buffer[data_count] = 0x00;
        break;
      }

      if (chr != '\n' && chr != 13)
        out_buffer[data_count++] = chr;

      time_out_count = 0;
    } else {

      if (time_out_count >= SER_TIME_OUT) {
        out_buffer[data_count] = 0x00;
        break;
      }
      
      time_out_count++;
    }
  }

  flush_software_serial();
  return data_count;
}

void sw_send_data(const char* str) {
  char packet[256];
  strcpy(packet, str);
  int packet_len = strlen(packet);
  packet[packet_len] = ';';
  packet[packet_len + 1] = 0x00;
  software_serial.print(packet);
}

#endif