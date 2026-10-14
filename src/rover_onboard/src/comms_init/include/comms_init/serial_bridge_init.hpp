#ifndef SERIAL_BRIDGE_INIT
#define SERIAL_BRIDGE_INIT

#include "CppLinuxSerial/SerialPort.hpp"
#include "events.hpp"
#include "ros_decl.hpp"

SharedSubscriber(Joystick, serial);

typedef mn::CppLinuxSerial::SerialPort SerialPort;
typedef mn::CppLinuxSerial::BaudRate BaudRate;

#define BAUDRATE 115200
#define SERIAL_PORT "/dev/ttyUSB0"

#endif
