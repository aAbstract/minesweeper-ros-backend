#ifndef MODELS
#define MODELS

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

#endif