// Update the CMakeLists and package.xml

// Implements
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "comms_init/events.hpp"
#include "comms_init/events.hpp"
#include "sensor_msgs/msg/nav_sat_fix.hpp"
#include "sensor_msgs/msg/nav_sat_status.hpp"

// Uses
#include <vector>
#include <memory>
#include <utility>
#include <chrono>
#include <libgpsmm.h>

// TODO: Move to a header.
#define SharedPublisher(TYPE, NAME) \
    typedef struct sharedPublisher { \
        TYPE pub; \
    } sharedPublisher_##NAME

#define UniquePtr(TYPE, CAST) \
    typedef struct uniquePtr { \
        std::unique_ptr<##TYPE> ptr; \
    } unique_##CAST

typedef sensor_msgs::msg::NavSatFix NavSatFix;
typedef sensor_msgs::msg::NavSatStatus NavSatStatus;

SharedPublisher(rclcpp::Publisher<NavSatFix>::SharedPtr, gps);
UniquePtr(NavSatFix, navSatFix);
UniquePtr(NavSatStatus, navSatStatus);


// For the timer period.
using namespace std::chrono_literals;
class GpsTelemNode : public rclcpp::Node 
{   
    private:
    sharedPublisher_gps _gps_publisher;
    unique_navSatFix _gps_telem;
    unique_navSatStatus _gps_status;

    rclcpp::TimerBase::SharedPtr _timer;
    std::chrono::milliseconds _period;

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
            gpsTelemProcess(_gps_telem.ptr);
    
            _gps_publisher.pub->publish(std::move(_gps_telem.ptr));

        };

        _period = 5ms;
        _gps_publisher.pub = this->create_publisher<NavSatFix>("gps-telem", qos_profile);
        _timer = this->create_wall_timer(_period, publish_gps_telem);
        
    }

    ~GpsTelemNode() {

    }

    void gpsTelemProcess(std::unique_ptr<sensor_msgs::msg::NavSatFix> &gps_ref)
    {
        // Populate data fields
        _gps_telem.ptr->latitude = 0.0;
        _gps_telem.ptr->longitude = 0.0;
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