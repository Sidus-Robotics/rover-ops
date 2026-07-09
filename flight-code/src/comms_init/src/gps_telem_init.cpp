// Update the CMakeLists and package.xml

// Implements
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "comms_init/events.hpp"
#include "comms_init/ros_decl.hpp"
#include "comms_init/gps_telem_init.hpp"

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
    sharedPublisher_gps _gps_publisher;
    unique_navSatFix _gps_telem;
    unique_navSatStatus _gps_status;

    clock_gps _clock;
    Milliseconds _period;

    // gpsmm gps_rec("localhost", GPSD_PORT);

    public:
    GpsTelemNode() : Node("gps-node") {
        //TODO: Make custom QoS profile

        rclcpp::QoS qos_profile(rclcpp::KeepLast(5));
        qos_profile.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile.durability(rclcpp::DurabilityPolicy::TransientLocal);

        auto publish_gps_telem = [this]() -> void 
        {
            _gps_telem.ptr = std::make_unique<NavSatFix>();
            gpsTelemProcess(_gps_telem);
    
            _gps_publisher.pub->publish(std::move(_gps_telem.ptr));

        };

        _period = 5ms;
        _gps_publisher.pub = this->create_publisher<NavSatFix>("gps-telem", qos_profile);
        _clock.timer = this->create_wall_timer(_period, publish_gps_telem);
        
    }

    ~GpsTelemNode() {

    }

    void gpsTelemProcess(unique_navSatFix &gps_ref)
    {
        // Populate data fields
        gps_ref.ptr->latitude = 0.0;
        gps_ref.ptr->longitude = 0.0;
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