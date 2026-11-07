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

import json
import re
import socket
import subprocess
import time
import uuid

import pygame


def get_wsl_ip():
    """Discover the current WSL IP address."""

    try:
        result = subprocess.run(
            ["wsl.exe", "sh", "-lc", "ip -4 route get 1.1.1.1"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )

        match = re.search(r"\bsrc\s+(\d+\.\d+\.\d+\.\d+)", result.stdout)

        if not match:
            raise RuntimeError("Could not find WSL IP address")

        ip = match.group(1)

        print(f"Discovered WSL IP: {ip}")
        return ip

    except Exception as e:
        raise RuntimeError(f"Failed to discover WSL IP: {e}")


def apply_deadzone(value: float, deadzone: float) -> float:
    if abs(value) < deadzone:
        return 0.0
    return round(value, 3)


def main():
    UDP_IP = get_wsl_ip()
    UDP_PORT = 8765
    RATE = 60.0
    DEADZONE = 0.1
    JOYSTICK_ID = 0

    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        raise RuntimeError("No controller detected")

    session_id = str(uuid.uuid4())
    joystick = pygame.joystick.Joystick(JOYSTICK_ID)

    print(f"Controller: {joystick.get_name()}")
    print(f"Axes: {joystick.get_numaxes()}")
    print(f"Buttons: {joystick.get_numbuttons()}")
    print(f"Sending UDP to {UDP_IP}:{UDP_PORT}")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination = (UDP_IP, UDP_PORT)

    sequence = 0
    period = 1.0 / RATE

    try:
        while True:
            loop_start = time.monotonic()

            # Update Pygame's controller state.
            pygame.event.pump()

            axes = [
                apply_deadzone(joystick.get_axis(i), DEADZONE)
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
