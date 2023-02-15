#ifndef SER_MAN
#define SER_MAN

#include <Arduino.h>

// config
#define DATA_PACKET_SIZE 21

struct input_serial_packet {
  int lax;
  int lay;
  int rax;
  int ray;
  char cmd;
};

struct output_serial_packet {
  int acc_x;
  int acc_y;
  int acc_z;
  char coil;
};

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
  const char lax_str[5] = {in_buffer[0], in_buffer[1], in_buffer[2],
                           in_buffer[3], 0x00};
  const char lay_str[5] = {in_buffer[5], in_buffer[6], in_buffer[7],
                           in_buffer[8], 0x00};
  const char rax_str[5] = {in_buffer[10], in_buffer[11], in_buffer[12],
                           in_buffer[13], 0x00};
  const char ray_str[5] = {in_buffer[15], in_buffer[16], in_buffer[17],
                           in_buffer[18], 0x00};
  const char cmd = in_buffer[20];

  // parse packet
  int lax, lay, rax, ray;
  sscanf(lax_str, "%4d", &lax);
  sscanf(lay_str, "%4d", &lay);
  sscanf(rax_str, "%4d", &rax);
  sscanf(ray_str, "%4d", &ray);

  // load object
  out_input_serial_packet.lax = lax;
  out_input_serial_packet.lay = lay;
  out_input_serial_packet.rax = rax;
  out_input_serial_packet.ray = ray;
  out_input_serial_packet.cmd = cmd;
  return 1;
}

void send_harware_serial_packet(
    const output_serial_packet& in_output_serial_packet) {
  char packet_buffer[128];
  sprintf(packet_buffer, "0000,0000,0000,%c", in_output_serial_packet.coil);
  int packet_len = strlen(packet_buffer);
  packet_buffer[packet_len] = ';';
  packet_buffer[packet_len + 1] = 0x00;
  Serial.print(packet_buffer);
}

#endif