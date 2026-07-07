// Update the CMakeLists and package.xml

// Implements
#include "rclcpp/rclcpp.hpp"

// Uses
#include <vector>
#include <memory>
#include <chrono>

class USBSerial : public rclcpp::Node
{
    private:
    public:
    USBSerial() : Node("usb-serial")
    {

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