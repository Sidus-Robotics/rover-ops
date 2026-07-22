#ifndef SERIAL_BRIDGE_INIT
#define SERIAL_BRIDGE_INIT

#include "events.hpp"
#include "ros_decl.hpp"
#include "CppLinuxSerial/SerialPort.hpp"

SharedSubscriber(Joystick, serial);

typedef mn::CppLinuxSerial::SerialPort SerialPort;
typedef mn::CppLinuxSerial::BaudRate BaudRate;

#define BAUDRATE 115200
#define SERIAL_PORT "/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"


#endif