#include <vector.h>
#include <memory>
#include <chrono>

#include <ixwebsocket/IXNetSystem.h>
#include <ixwebsocket/IXWebSocket.h>
#include <ixwebsocket/IXUserAgent.h>
#include <iostream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.h"

class WebSocketNode: public rclcpp::Node{
    public:
    WebSocketNode() : Node("websocket-node") {
        //TODO: Make custom QoS profile
        auto topic_cb = [this](std_msgs::msg::String::UniquePtr msg) -> void {
            RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());



        };
        request_publisher_ = this->create_publisher<std_msgs::msg::String>("web-request", qos_profile);
        response_subscription_ = this->create_subscription<std_msgs::msg::String>("web-response", qos_profile);
    }

    private:
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr request_publisher_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr response_subscription_;

};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<WebSocketNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}