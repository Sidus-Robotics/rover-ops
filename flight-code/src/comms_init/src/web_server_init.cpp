#include <vector.h>
#include <memory>
#include <chrono>

#include <ixwebsocket/IXNetSystem.h>
#include <ixwebsocket/IXWebSocket.h>
#include <ixwebsocket/IXUserAgent.h>
#include <iostream>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class WebSocketNode: public rclcpp::Node{
    public:
    WebSocketNode() : Node("websocket-node") {
        //TODO: Make custom QoS profile

        rclcpp::QoS qos_profile_req(rclcpp::KeepLast(5));
        qos_profile_req.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile_req.durability(rclcpp::DurabilityPolicy::TransientLocal);

        rclcpp::QoS qos_profile_res(rclcpp::KeepLast(5));
        qos_profile_res.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile_res.durability(rclcpp::DurabilityPolicy::TransientLocal);

        auto topic_cb = [this](std_msgs::msg::String::UniquePtr msg) {
            RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());
        };

        request_publisher_ = this->create_publisher<std_msgs::msg::String>("web-request", qos_profile_req);
        response_subscription_ = this->create_subscription<std_msgs::msg::String>("web-response", qos_profile_res, topic_cb);
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