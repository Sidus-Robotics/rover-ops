"""
Controller bridge for Windows.

This is a helper script to allow for usb devices (i.e. controllers)
to be used within WSL.

DEPENDANCIES:
- pygame-ce

USAGE:
- Run this script seperately in WINDOWS (not WSL).
- Run the controller bridge listener node within WSL.
"""

import argparse
import json
import socket
import time
import uuid

import pygame


def apply_deadzone(value: float, deadzone: float) -> float:
    if abs(value) < deadzone:
        return 0.0
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1", help="ROS 2 receiver IP address")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--rate", type=float, default=60.0)
    parser.add_argument("--deadzone", type=float, default=0.1)
    parser.add_argument("--joystick", type=int, default=0, help="Pygame joystick index")
    args = parser.parse_args()

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        raise RuntimeError("No controller detected")

    session_id = str(uuid.uuid4())
    joystick = pygame.joystick.Joystick(args.joystick)

    print(f"Controller: {joystick.get_name()}")
    print(f"Axes: {joystick.get_numaxes()}")
    print(f"Buttons: {joystick.get_numbuttons()}")
    print(f"Sending UDP to {args.host}:{args.port}")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination = (args.host, args.port)

    sequence = 0
    period = 1.0 / args.rate

    try:
        while True:
            loop_start = time.monotonic()

            # Update Pygame's controller state.
            pygame.event.pump()

            axes = [
                apply_deadzone(joystick.get_axis(i), args.deadzone)
                for i in range(joystick.get_numaxes())
            ]

            buttons = [
                int(joystick.get_button(i)) for i in range(joystick.get_numbuttons())
            ]

            packet = {
                "session_id": session_id,
                "sequence": sequence,
                "connected": True,
                "axes": axes,
                "buttons": buttons,
            }

            encoded = json.dumps(packet).encode("utf-8")
            udp_socket.sendto(encoded, destination)

            sequence += 1

            # Maintain the requested update frequency.
            elapsed = time.monotonic() - loop_start
            time.sleep(max(0.0, period - elapsed))

    except KeyboardInterrupt:
        print("\nController bridge stopped.")

    finally:
        # Best-effort neutral/disconnected packet.
        try:
            packet = {
                "sequence": sequence,
                "connected": False,
                "axes": [0.0] * joystick.get_numaxes(),
                "buttons": [0] * joystick.get_numbuttons(),
            }
            udp_socket.sendto(
                json.dumps(packet).encode("utf-8"),
                destination,
            )
        except OSError:
            pass

        udp_socket.close()
        joystick.quit()
        pygame.quit()


if __name__ == "__main__":
    main()
