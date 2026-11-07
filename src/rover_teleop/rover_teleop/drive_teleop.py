import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy


class DriveTeleopNode(Node):
    def __init__(self):
        super().__init__("drive_teleop")
        self.joy_subscriber_ = self.create_subscription(
            Joy, "joy", self.callback_joy, 10
        )
        self.get_logger().info("Drive motor teleoperation started.")

    def callback_joy(self, msg: Joy):
        self.get_logger().info(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DriveTeleopNode()
    rclpy.spin(node)
    rclpy.shutdown()
