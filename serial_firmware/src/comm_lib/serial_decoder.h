#ifndef SERIAL_DECODER
#define SERIAL_DECODER

#include <Arduino.h>
#include "./models.h"

// serial input packet shape
// 0000,0000,0000,0000,0--
// LAX-:LAY-:RAX-:RAY-:CMD

void decode_input_serial_packet(char* in_buffer,
                                input_serial_packet& out_input_serial_packet) {
  // packet breaddown
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
}

// serial output packet shape
// ACCX:ACCY:ACCZ:COIL
// 0000,0000,0000,0---

void encode_output_serial_packet(
    const output_serial_packet& in_output_serial_packet,
    char* out_buffer) {
  sprintf(out_buffer, "0000,0000,0000,%c", in_output_serial_packet.coil);
}

#endif