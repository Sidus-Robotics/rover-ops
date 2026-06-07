// Implements
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

// Uses
#include <vector>
#include <chrono>

class CameraNode : public rclcpp::Node {
    public:
    CameraNode() : Node("camera_node") {
        return;
    }
    ~CameraNode() {
        return;
    }
    private:
};

int main(int argc, char **argv) {
    return 0;
}