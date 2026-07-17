#ifndef EVENTS
#define EVENTS
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"
#include "sensor_msgs/msg/nav_sat_status.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/byte.hpp"

#include "ros_decl.hpp"

#include <chrono>

#define GPSD_PORT 8080
#define URL "ws://127.0.0.1:8000/rover-obc"

typedef sensor_msgs::msg::NavSatFix NavSatFix;
typedef sensor_msgs::msg::NavSatStatus NavSatStatus;

/**
 * @brief std_msgs::msg::String
 * 
 */
typedef std_msgs::msg::String String;

/**
 * @brief std_msgs::msg::Byte
 */
typedef std_msgs::msg::Byte Byte;

typedef std::chrono::milliseconds Milliseconds;

#endif