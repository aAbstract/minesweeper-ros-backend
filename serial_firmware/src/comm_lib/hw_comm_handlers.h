#ifndef HW_COMM_HANDLERS
#define HW_COMM_HANDLERS

#include "./hw_serial.h"
#include "./models.h"
// #include "./motors_lib/motors.h"
#include "./serial_decoder.h"

// config
#define COIL_PIN A0
#define BUZZER_PIN A1

unsigned long int last_tic = 0;
int dt_limit = 3000;

void encode_and_send_reading(
    const output_serial_packet& in_output_serial_packet) {
  char packet_buffer[128];
  encode_output_serial_packet(in_output_serial_packet, packet_buffer);
  hw_send_data(packet_buffer);
}

void handle_input_serial_packet() {
  if (Serial.available() > 0) {
    input_serial_packet in_input_serial_packet;
    int decode_success = read_hardware_serial_packet(in_input_serial_packet);

    if (!decode_success)
      return;

    // print input serial packet handler
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
    Serial.println(in_input_serial_packet.cmd);

    // // cmd handler

    if (in_input_serial_packet.cmd == 'W') {
      digitalWrite(BUZZER_PIN, 1);
      Serial.println("Buzzer On");
    } else {
      digitalWrite(BUZZER_PIN, 0);
      Serial.println("Buzzer Off");
    }

    // if (in_input_serial_packet.cmd == 'W')
    //   forward();
    // else if (in_input_serial_packet.cmd == 'D')
    //   right();
    // else if (in_input_serial_packet.cmd == 'S')
    //   backward();
    // else if (in_input_serial_packet.cmd == 'A')
    //   left();
    // else if (in_input_serial_packet.cmd == 'X')
    //   zero();
  }
}

void handle_output_serial_packet() {
  int dt = millis() - last_tic;

  if (dt < dt_limit)
    return;

  last_tic = millis();

  int coil_val = analogRead(COIL_PIN);

  if (coil_val >= 200) {
    digitalWrite(BUZZER_PIN, 1);

    // construct output serial packet
    output_serial_packet in_output_serial_packet;
    in_output_serial_packet.coil = '1';

    encode_and_send_reading(in_output_serial_packet);
  } else {
    digitalWrite(BUZZER_PIN, 0);

    // construct output serial packet
    output_serial_packet in_output_serial_packet;
    in_output_serial_packet.coil = '0';

    encode_and_send_reading(in_output_serial_packet);
  }
}

#endif