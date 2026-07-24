// Update the CMakeLists and package.xml

// Implements
#include "rclcpp/rclcpp.hpp"
#include "comms_init/serial_bridge_init.hpp"

// Uses
#include <vector>
#include <memory>
#include <chrono>

class USBSerial : public rclcpp::Node
{
    private:
    sharedSubscriber_serial _serial;
    SerialPort _serialDevice;
    
    public:
    USBSerial() : Node("usb_serial"), _serialDevice(SERIAL_PORT, BAUDRATE) 
    {
        //TODO: Make custom QoS profile
        _serialDevice.SetTimeout(10);
        _serialDevice.Open();

        rclcpp::QoS qos_profile(rclcpp::KeepLast(5));
        qos_profile.reliability(rclcpp::ReliabilityPolicy::BestEffort);
        qos_profile.durability(rclcpp::DurabilityPolicy::TransientLocal);

        auto responseHandler = [this](Joystick::UniquePtr msg) -> void
        {   
            std::string payload;

            for (uint8_t index = 0; index < msg->axes.size(); index++)
            {
                char value = msg->axes.at(index);
                RCLCPP_INFO(this->get_logger(), "Logging value: %f", value);
                _serialDevice.WriteBinary(msg->axes);
                payload.append(std::to_string(value));
            }
            _serialDevice.Write(payload);
   
        };

        _serial.sub = this->create_subscription<Joystick>("serial_request", qos_profile, responseHandler);
        RCLCPP_INFO(this->get_logger(), "serial_request node started.");
    }

    ~USBSerial()
    {
        _serialDevice.Close();
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