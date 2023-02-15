#ifndef SW_COMM_HANDLERS
#define SW_COMM_HANDLERS

#include "./models.h"
#include "./serial_decoder.h"
#include "./sw_serial.h"

// config
#define DATA_PACKET_SIZE 21

unsigned long int last_tic = 0;
int dt_limit = 3000;

void encode_and_send_reading(
    const output_serial_packet& in_output_serial_packet) {
  char packet_buffer[128];
  encode_output_serial_packet(in_output_serial_packet, packet_buffer);
  sw_send_data(packet_buffer);
}

void handle_input_serial_packet() {
  if (software_serial.available() > 0) {
    // read serial packet
    char in_buffer[128];
    int data_len = read_software_serial(in_buffer);

    Serial.print("received: ");
    Serial.println(in_buffer);

    if (data_len != DATA_PACKET_SIZE)
      return;

    // decode serial packet
    input_serial_packet in_input_serial_packet;
    decode_input_serial_packet(in_buffer, in_input_serial_packet);

    // handler: print input serial packet
    char print_buffer[256];
    sprintf(print_buffer,
            "LAX: %d\n"
            "LAY: %d\n"
            "RAX: %d\n"
            "RAY: %d\n"
            "cmd: %c",
            in_input_serial_packet.lax, in_input_serial_packet.lay,
            in_input_serial_packet.rax, in_input_serial_packet.ray,
            in_input_serial_packet.cmd);
    Serial.println(print_buffer);
  }
}

void handle_output_serial_packet() {
  int dt = millis() - last_tic;

  if (dt < dt_limit)
    return;

  last_tic = millis();

  // construct output serial packet
  output_serial_packet in_output_serial_packet;
  in_output_serial_packet.coil = '1';

  encode_and_send_reading(in_output_serial_packet);
}

#endif