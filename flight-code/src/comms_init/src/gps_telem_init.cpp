// Update the CMakeLists and package.xml

// Implements
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "comms_init/events.hpp"

// Uses
#include <vector>
#include <memory>
#include <chrono>
#include <libgpsmm.h>

// TODO: Create custom GPS telem msg interface.

class GpsTelemNode : public rclcpp::Node 
{   
    private:
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr _gps_publisher;
    std::unique_ptr<std_msgs::msg::String> _gps_telem;
    rclcpp::TimerBase::SharedPtr _timer;

    public:
    GpsTelemNode() : Node("gps-node") {
        //TODO: Make custom QoS profile

        rclcpp::QoS qos_profile(rclcpp::KeepLast(5));
        qos_profile.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile.durability(rclcpp::DurabilityPolicy::TransientLocal);

        _gps_publisher = this->create_publisher<std_msgs::msg::String>("gps-telem", qos_profile);

        
    }

    ~GpsTelemNode() {

    }

    void gpsTelemProcess
    {

    }

    void gpsNodeCleanup()
    {
        return;
    }
};


int main(int argc, char **argv) 
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<GpsTelemNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}