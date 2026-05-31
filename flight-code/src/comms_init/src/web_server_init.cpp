#include <vector>
#include <memory>
#include <chrono>

#include <ixwebsocket/IXNetSystem.h>
#include <ixwebsocket/IXWebSocket.h>
#include <ixwebsocket/IXUserAgent.h>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

static const std::string URL = "ws://localhost:3000/";

class WebSocketNode: public rclcpp::Node{
    public:
    WebSocketNode() : Node("websocke_node") {
        //Establish Websocket connection

        web_socket_.setUrl(URL);
        web_socket_.setOnMessageCallback([this](const ix::WebSocketMessagePtr &msg){
            this->webServerCallbackHandler(msg);
        });
        web_socket_.start();
        //TODO: Make custom QoS profile

        rclcpp::QoS qos_profile_res(rclcpp::KeepLast(5));
        qos_profile_res.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile_res.durability(rclcpp::DurabilityPolicy::TransientLocal);

        request_publisher_ = this->create_publisher<std_msgs::msg::String>("web_request", qos_profile_res);
        RCLCPP_INFO(this->get_logger(), "web_request node started.");
    }

    void webServerCallbackHandler(const ix::WebSocketMessagePtr& msg) {
        if (msg->type == ix::WebSocketMessageType::Message)
            {
                RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->str.c_str());

                //Change types
                
                std_msgs::msg::String request_message;

                request_message.data = msg->str;

                this->request_publisher_->publish(request_message);
            }
        return;
    };

    private:
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr request_publisher_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr response_subscription_;
    ix::WebSocket web_socket_;

};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<WebSocketNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}