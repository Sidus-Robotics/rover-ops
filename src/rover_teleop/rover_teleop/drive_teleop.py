import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Joy


class DriveTeleopNode(Node):
    def __init__(self):
        super().__init__("drive_teleop")

        self.joy_subscriber = self.create_subscription(
            Joy, "joy", self.callback_joy, 10
        )

        self.cmd_vel_publisher = self.create_publisher(Twist, "cmd_vel", 10)
        self.create_timer(1 / 60, self.publish_cmd_vel)

        # msg.Twist Stucture
        self.linear = [0.0, 0.0, 0.0]
        self.angular = [0.0, 0.0, 0.0]

        self.get_logger().info("Drive motor teleoperation started.")

    def callback_joy(self, msg: Joy):
        axes = msg.axes.tolist()
        # buttons = msg.buttons.tolist()

        # left_stick_x = axes[0]
        # left_stick_y = axes[1]
        # right_stick_x = axes[2]
        # right_stick_y = axes[3]

        left_trigger = axes[4]
        right_trigger = axes[5]

        # btn_a = buttons[0]
        # btn_b = buttons[1]
        # btn_x = buttons[2]
        # btn_y = buttons[3]

        # Scale values
        if left_trigger > 0:
            self.linear[0] = self.scale(-left_trigger)
        elif right_trigger > 0:
            self.linear[0] = self.scale(right_trigger)
        else:
            self.linear[0] = 0.0

    def publish_cmd_vel(self):
        msg = Twist()

        # Drive forward / back
        msg.linear.x = self.linear[0]
        # Steering
        msg.angular.z = self.angular[2]

        self.cmd_vel_publisher.publish(msg)

        self.get_logger().info(
            f"Published cmd_vel | linear.x: {self.linear[0]} , angular.z: {self.angular[2]}"
        )

    def scale(
        self,
        value,
        input_range=(-1.0, 1.0),
        target_range=(-1023, 1023),
        neutral_range=(-15, 15),
    ):
        """Scale controller input to motor output range, with a neutral deadzone."""

        from_min, from_max = input_range
        to_min, to_max = target_range

        scaled_value = ((value - from_min) / (from_max - from_min)) * (
            to_max - to_min
        ) + to_min

        # Apply neutral range deadzone
        if neutral_range[0] <= scaled_value <= neutral_range[1]:
            return 0.0

        return float(scaled_value)


def main(args=None):
    rclpy.init(args=args)
    node = DriveTeleopNode()
    rclpy.spin(node)
    rclpy.shutdown()
