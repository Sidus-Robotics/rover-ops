import json
import socket
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy


class UdpReceiver(Node):
    """
    UDP RECEIVER NODE.

    This is a node to receive controller data from a windows computer inside the devcontainer.

    Use in conjuntion with the controller_bridge.py util script.
    See README and example usage in utils/controller_bridge/
    """

    def __init__(self):
        super().__init__("udp_receiver")

        # Paramerters (useful for launch files)
        self.declare_parameter("port", 8765)
        self.declare_parameter("packet_timeout", 0.25)
        self.declare_parameter("publish_rate", 60.0)
        self.declare_parameter("default_axes", 6)
        self.declare_parameter("default_buttons", 15)

        port = self.get_parameter("port").get_parameter_value().integer_value
        timeout = (
            self.get_parameter("packet_timeout").get_parameter_value().double_value
        )
        publish_rate = (
            self.get_parameter("publish_rate").get_parameter_value().double_value
        )
        self.default_axes = (
            self.get_parameter("default_axes").get_parameter_value().integer_value
        )
        self.default_buttons = (
            self.get_parameter("default_buttons").get_parameter_value().integer_value
        )

        self.packet_timeout = float(timeout)

        # PUBLISHER
        self.joy_publisher = self.create_publisher(Joy, "/joy", 10)

        # UDP socket
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.bind(("0.0.0.0", port))
        self.udp_socket.setblocking(False)

        self.axes = [0.0] * self.default_axes
        self.buttons = [0] * self.default_buttons

        self.last_packet_time = None
        self.last_sequence = None
        self.session_id = None
        self.connected = False

        self.create_timer(0.005, self.receive_packets)
        self.create_timer(1.0 / publish_rate, self.publish_joy)

        self.get_logger().info(f"UDP receiver listening on port {port}")

    def receive_packets(self):
        """Read all currently available UDP packets."""
        while True:
            try:
                data, _address = self.udp_socket.recvfrom(4096)

            except BlockingIOError:
                break

            try:
                packet = json.loads(data.decode("utf-8"))

                session_id = packet["session_id"]
                sequence = packet["sequence"]
                connected = packet["connected"]
                axes = packet["axes"]
                buttons = packet["buttons"]

                if session_id != self.session_id:
                    self.session_id = session_id
                    self.last_sequence = None

                if self.last_sequence is not None and sequence <= self.last_sequence:
                    self.get_logger().warning(f"Out-of-order packet: {sequence}")
                    continue

                self.last_sequence = sequence
                self.last_packet_time = time.monotonic()
                self.connected = connected

                if connected:
                    self.axes = list(axes)
                    self.buttons = list(buttons)
                else:
                    self.axes = [0.0] * max(len(axes), self.default_axes)
                    self.buttons = [0] * max(len(buttons), self.default_buttons)

                self.get_logger().info(
                    f"Accepted packet {sequence}: "
                    f"axes={self.axes}, buttons={self.buttons}"
                )

            except (KeyError, ValueError, TypeError, UnicodeDecodeError) as exc:
                self.get_logger().warning(f"Discarded UDP packet: {exc}")

    def publish_joy(self):
        """Publish the latest controller state, or neutral input on timeout."""
        # If packet took too long to recieve (longer than the timeout specified) return False
        packet_is_fresh = (
            self.last_packet_time is not None
            and time.monotonic() - self.last_packet_time < self.packet_timeout
        )

        # Joy msg type structure: https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Joy.html
        msg = Joy()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "controller"

        if packet_is_fresh and self.connected:
            msg.axes = self.axes
            msg.buttons = self.buttons
        else:
            # No recent packet or controller disconnected
            msg.axes = [0.0] * max(len(self.axes), self.default_axes)
            msg.buttons = [0] * max(len(self.buttons), self.default_buttons)

        self.joy_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = UdpReceiver()
    rclpy.spin(node)
    node.udp_socket.close()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
