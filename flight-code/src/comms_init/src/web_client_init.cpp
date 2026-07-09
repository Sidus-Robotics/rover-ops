// Implements
#include "comms_init/events.hpp"

// Uses
#include <vector>
#include <memory>
#include <chrono>

#include <ixwebsocket/IXWebSocket.h>
class WebSocketNode: public rclcpp::Node{

    private:
    rclcpp::Publisher<String>::SharedPtr _request_publisher;
    rclcpp::Subscription<String>::SharedPtr response_subscription_;
    ix::WebSocket _web_socket;
    ix::WebSocketHttpHeaders _header;

    public:
    WebSocketNode() : Node("websocket_node") {
        //TODO: Make custom QoS profile

        rclcpp::QoS qos_profile_res(rclcpp::KeepLast(5));
        qos_profile_res.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile_res.durability(rclcpp::DurabilityPolicy::TransientLocal);

        rclcpp::QoS qos_profile_req(rclcpp::KeepLast(5));
        qos_profile_req.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile_req.durability(rclcpp::DurabilityPolicy::TransientLocal);

        auto responseHandler = [this](String::UniquePtr msg){
            _web_socket.send(msg->data);
        };


        response_subscription_ = this->create_subscription<String>("web_response", qos_profile_res, responseHandler);
        _request_publisher = this->create_publisher<String>("web_request", qos_profile_req);
        RCLCPP_INFO(this->get_logger(), "web_request node started.");

        webServerConnect();
    }

    ~WebSocketNode() {
        webConnectionCleanup();
    }

    void webServerConnect() {
        //Establish Websocket connection

        _header["client-id"] = "rover-obc";

        _web_socket.setUrl(URL);
        _web_socket.setExtraHeaders(_header);
        _web_socket.setOnMessageCallback([this](const ix::WebSocketMessagePtr &msg){
            this->webServerHandler(msg);
        });
        _web_socket.start();
        std::string test_msg = "Testing connect...";
        _web_socket.send(test_msg);
        RCLCPP_INFO(this->get_logger(), "websocket started on '%s'.", URL);

        return;
    }

    void webServerHandler(const ix::WebSocketMessagePtr& msg) {
        if (msg->type == ix::WebSocketMessageType::Message)
            {
                RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->str.c_str());

                //Change types
                
                String request_message;

                request_message.data = msg->str;

                this->_request_publisher->publish(request_message);
            }
        return;
    };

    void webConnectionCleanup() {
        //TODO add cleanup aka destroy the connection cleanly.
        _web_socket.stop(1000, "Normal Closure.");
        return;
    };

};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<WebSocketNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}