#ifndef GPS_TELEM_INIT
#define GPS_TELEM_INIT
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"
#include "sensor_msgs/msg/nav_sat_status.hpp"

#include "ros_decl.hpp"

typedef sensor_msgs::msg::NavSatFix NavSatFix;
typedef sensor_msgs::msg::NavSatStatus NavSatStatus;

SharedPublisher(rclcpp::Publisher<NavSatFix>::SharedPtr, gps);
UniquePtr(NavSatFix, navSatFix);
UniquePtr(NavSatStatus, navSatStatus);

#endif