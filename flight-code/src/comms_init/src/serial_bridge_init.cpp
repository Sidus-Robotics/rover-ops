// Update the CMakeLists and package.xml

// Implements
#include "rclcpp/rclcpp.hpp"
#include "serialib/serialib.h"
#include "comms_init/serial_bridge_init.hpp"

// Uses
#include <vector>
#include <memory>
#include <chrono>

#define PORT "/dev/ttyUSB0"
#define BAUD 115200
class USBSerial : public rclcpp::Node
{
    private:
    sharedSubscriber_serial _serial;
    serialib _serialDevice;
    
    public:
    USBSerial() : Node("usb-serial")
    {
        //TODO: Make custom QoS profile

        rclcpp::QoS qos_profile(rclcpp::KeepLast(5));
        qos_profile.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile.durability(rclcpp::DurabilityPolicy::TransientLocal);

        _serialDevice.openDevice(PORT, BAUD);

        auto responseHandler = [this](Byte::ConstPtr msg) -> void
        {
            // TODO: Implement, needs a byte array. 

            _serialDevice.writeBytes(msg->data, 8);
        };

        _serial.sub = this->create_subscription<Byte>("web-request", qos_profile, responseHandler);
    }

    ~USBSerial()
    {

    }

};


int main(int argc, char **argv) 
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<USBSerial>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}