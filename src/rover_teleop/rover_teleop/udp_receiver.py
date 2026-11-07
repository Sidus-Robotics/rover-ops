import json
import math
import socket
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy


class UdpJoyReceiver(Node):
    def __init__(self):
        super().__init__("udp_receiver")

        self.declare_parameter("port", 8765)
        self.declare_parameter("packet_timeout", 0.25)
        self.declare_parameter("publish_rate", 60.0)
        self.declare_parameter("default_axes", 6)
        self.declare_parameter("default_buttons", 16)

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

        self.joy_publisher = self.create_publisher(Joy, "/joy", 10)

        # UDP socket.
        self.udp_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
        )
        self.udp_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
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

        self.get_logger().info(f"UDP joystick receiver listening on port {port}")

    def receive_packets(self):
        """Read all currently available UDP packets."""
        while True:
            try:
                data, _sender = self.udp_socket.recvfrom(4096)
            except BlockingIOError:
                break

            try:
                packet = json.loads(data.decode("utf-8"))

                sequence = packet["sequence"]
                session_id = packet["session_id"]
                connected = packet["connected"]
                axes = packet["axes"]
                buttons = packet["buttons"]

                # Basic structure validation.
                if not isinstance(sequence, int) or sequence < 0:
                    continue

                if not isinstance(session_id, str) or not session_id:
                    continue

                if not isinstance(connected, bool):
                    continue

                if not isinstance(axes, list) or len(axes) > 64:
                    continue

                if not isinstance(buttons, list) or len(buttons) > 64:
                    continue

                # Validate axis values.
                if not all(
                    isinstance(value, (int, float))
                    and not isinstance(value, bool)
                    and math.isfinite(value)
                    and -1.0 <= value <= 1.0
                    for value in axes
                ):
                    continue

                # Validate button values.
                if not all(
                    isinstance(value, int)
                    and not isinstance(value, bool)
                    and value in (0, 1)
                    for value in buttons
                ):
                    continue

                # A new bridge session allows sequence numbers to restart.
                if session_id != self.session_id:
                    self.session_id = session_id
                    self.last_sequence = None

                # Reject duplicate or out-of-order packets.
                if self.last_sequence is not None and sequence <= self.last_sequence:
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

            except (KeyError, ValueError, TypeError, UnicodeDecodeError):
                self.get_logger().warning("Discarded malformed UDP packet")

    def publish_joy(self):
        """Publish the latest controller state, or neutral input on timeout."""
        packet_is_fresh = (
            self.last_packet_time is not None
            and time.monotonic() - self.last_packet_time < self.packet_timeout
        )

        msg = Joy()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "controller"

        if packet_is_fresh and self.connected:
            msg.axes = self.axes
            msg.buttons = self.buttons
        else:
            # No recent packet or controller disconnected.
            msg.axes = [0.0] * max(len(self.axes), self.default_axes)
            msg.buttons = [0] * max(len(self.buttons), self.default_buttons)

        self.joy_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = UdpJoyReceiver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.udp_socket.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
