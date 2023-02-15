#include <Arduino.h>
#include "./serial_man.h"

#define COIL_PIN A0
#define BUZZER_PIN A1
#define COIL_DT 1000

unsigned long int last_tic = 0;

void handle_coil() {
  // handle coil reading
  int dt = millis() - last_tic;

  if (dt < COIL_DT)
    return;

  last_tic = millis();

  int coil_val = analogRead(COIL_PIN);

  if (coil_val >= 200) {
    digitalWrite(BUZZER_PIN, 1);

    // construct output serial packet
    output_serial_packet in_output_serial_packet;
    in_output_serial_packet.coil = '1';

    send_harware_serial_packet(in_output_serial_packet);
  } else {
    digitalWrite(BUZZER_PIN, 0);

    // construct output serial packet
    output_serial_packet in_output_serial_packet;
    in_output_serial_packet.coil = '0';

    send_harware_serial_packet(in_output_serial_packet);
  }
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  // handle input packet
  if (Serial.available() > 0) {
    input_serial_packet in_input_serial_packet;
    int decode_success = read_hardware_serial_packet(in_input_serial_packet);

    if (!decode_success)
      return;

    Serial.println(in_input_serial_packet.cmd);
  }

  handle_coil();
}