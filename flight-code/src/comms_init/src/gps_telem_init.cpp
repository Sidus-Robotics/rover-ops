// Update the CMakeLists and package.xml

// Implements
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "comms_init/events.hpp"
#include "comms_init/events.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"

// Uses
#include <vector>
#include <memory>
#include <utility>
#include <chrono>
#include <libgpsmm.h>

// For the timer period.
using namespace std::chrono_literals;
class GpsTelemNode : public rclcpp::Node 
{   
    private:
    rclcpp::Publisher<sensor_msgs::msg::NavSatFix>::SharedPtr _gps_publisher;
    std::shared_ptr<sensor_msgs::msg::NavSatFix> _gps_telem;
    rclcpp::TimerBase::SharedPtr _timer;
    std::chrono::milliseconds _period;

    gpsmm gps_rec("localhost", GPSD_PORT);

    public:
    GpsTelemNode() : Node("gps-node") {
        //TODO: Make custom QoS profile

        rclcpp::QoS qos_profile(rclcpp::KeepLast(5));
        qos_profile.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile.durability(rclcpp::DurabilityPolicy::TransientLocal);

        auto publish_gps_telem = [this]() -> void 
        {
            _gps_telem = std::make_shared<sensor_msgs::msg::NavSatFix>();
            gpsTelemProcess(_gps_telem);
            auto _msg = std::make_unique<sensor_msgs::msg::NavSatFix>(std::(_gps_telem->latitude));
            // Populate data fields
            _gps_telem->latitude = 0.0;
            _gps_telem->longitude = 0.0;

            _gps_publisher->publish(_gps_telem);

        };

        _period = 5ms;
        _gps_publisher = this->create_publisher<sensor_msgs::msg::NavSatFix>("gps-telem", qos_profile);
        _timer = this->create_wall_timer(_period, publish_gps_telem);
        
    }

    ~GpsTelemNode() {

    }

    void gpsTelemProcess(std::shared_ptr<sensor_msgs::msg::NavSatFix> &gps_ref)
    {
        return;
    };

    void gpsNodeCleanup()
    {
        return;
    };
};


int main(int argc, char **argv) 
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<GpsTelemNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}