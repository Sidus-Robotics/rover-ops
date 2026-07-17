#ifndef SERIAL_BRIDGE_INIT
#define SERIAL_BRIDGE_INIT

#include "events.hpp"
#include "ros_decl.hpp"

SharedSubscriber(rclcpp::Subscription<Byte>::SharedPtr, serial);

#endif