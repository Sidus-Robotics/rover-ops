// Update the CMakeLists and package.xml

// Implements
#include "rclcpp/rclcpp.hpp"

// Uses
#include <vector>
#include <memory>
#include <chrono>


class GpsTelemNode : public rclcpp::Node 
{   
    private:

    public:
    GpsTelemNode() : Node("gps-telem") {

    }

    ~GpsTelemNode() {

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