#ifndef EVENTS
#define EVENTS
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"
#include "sensor_msgs/msg/nav_sat_status.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/byte.hpp"
#include "rover_interfaces/msg/controller.hpp"

#include "ros_decl.hpp"

#include <chrono>

#define GPSD_PORT 8080

// Rovers Bullet AC Static IP
#define URL "ws://192.168.1.19:8000/rover-obc"

typedef sensor_msgs::msg::NavSatFix NavSatFix;
typedef sensor_msgs::msg::NavSatStatus NavSatStatus;

/**
 * @brief std_msgs::msg::String
 * 
 * This is a temporary solution. All std_msgs interfaces are deprecated since Foxy.
 */
typedef std_msgs::msg::String String;

/**
 * @brief rover_interfaces::msg::Controller
 * 
 * float32[] axes and int32[] buttons
 */
typedef rover_interfaces::msg::Controller Joystick;

typedef std::chrono::milliseconds Milliseconds;

#endif