import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class Esp32SerialBridgeNode(Node):
    def __init__(self):
        super().__init__("esp32_serial_bridge")
        self.cmd_vel_subscriber_ = self.create_subscription(
            Twist, "cmd_vel", self.callback_cmd_vel, 10
        )
        self.get_logger().info("Drive motor teleoperation started.")

    def callback_cmd_vel(self, msg: Twist):
        # TODO: Send over serial to the esp32...
        self.get_logger().info(f"{msg.linear}")


def main(args=None):
    rclpy.init(args=args)
    node = Esp32SerialBridgeNode()
    rclpy.spin(node)
    rclpy.shutdown()
