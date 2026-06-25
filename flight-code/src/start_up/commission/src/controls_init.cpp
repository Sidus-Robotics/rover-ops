// Implements
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

// Uses
#include <vector>
#include <chrono>

class ControlNode : public rclcpp::Node {
    public:
    ControlNode() : Node("camera_node") {
        return;
    }
    ~ControlNode() {
        return;
    }
    private:
};

int main(int argc, char **argv) {
    return 0;
}