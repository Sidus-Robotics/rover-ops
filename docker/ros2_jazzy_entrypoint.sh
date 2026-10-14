#!/bin/bash
set -e

# shellcheck disable=SC1091
source /opt/ros/jazzy/setup.bash

if [ -e "/ros2_ws/install/setup.bash" ]; then
    # shellcheck disable=SC1091
    source /ros2_ws/install/setup.bash
fi

if [ "$ENABLE_VNC" = "1" ]; then
    /usr/local/bin/start-vnc
fi

exec "$@"