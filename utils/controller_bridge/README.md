
# Controller bridge for Windows.

This is a helper script to allow for usb devices (i.e. controllers) to be used within WSL and the devcontainer.

## Dependencies:
- `pygame-ce`

## Example Usage:
Run this script seperately in WINDOWS (not WSL).
```PS
python3 controller_bridge.py
```
Inside the **devcontainer** run the following:
```bash
colcon build --select-packages rover_teleop
source install/setup.bash
ros2 run rover_teleop udp_receiver
```